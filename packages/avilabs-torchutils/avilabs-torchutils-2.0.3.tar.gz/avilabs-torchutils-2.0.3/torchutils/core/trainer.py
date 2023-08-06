import logging
from dataclasses import dataclass
from typing import Callable, Sequence

import mlflow
import mlflow.pytorch
import numpy as np
import torch as t
from torch.utils.data import DataLoader, Dataset

from .hyperparams import Hyperparams

MetricFunc = Callable[[Sequence[float], Sequence[float]], float]


@dataclass
class TrainerArgs:
    run_name: str
    model: t.nn.Module
    optim: t.optim.Optimizer
    loss_fn: Callable[[t.Tensor, t.Tensor], t.Tensor]
    trainloader: DataLoader
    valloader: DataLoader
    n_epochs: int
    grad_warning_threshold: float = 1000
    loss_warning_threshold: float = 10_000


ArgsBuilderType = Callable[[Hyperparams, Dataset, Dataset], TrainerArgs]

DEVICE = t.device("cuda" if t.cuda.is_available() else "cpu")


class Trainer:
    def __init__(
        self, exp_name: str, trainset: Dataset, valset: Dataset, metrics: Sequence[MetricFunc]
    ):
        mlflow.set_experiment(exp_name)
        logging.info(f"Experiment set to {exp_name}")
        self._trainset = trainset
        self._valset = valset
        self._metrics = metrics

        self.log_frequency = 10

        self.model = None
        self.model_path = None
        self.final_val_metrics = []

    def train(self, hparams: Hyperparams, args_builder: ArgsBuilderType, save_model=True):
        self.model = None
        self.model_path = None
        self.final_val_metrics = []

        args = args_builder(hparams, self._trainset, self._valset)
        model = args.model.to(DEVICE)
        optim = args.optim
        loss_fn = args.loss_fn
        traindl = args.trainloader
        valdl = args.valloader
        n_epochs = args.n_epochs

        with mlflow.start_run(run_name=args.run_name) as run:
            logging.info(f"Starting run {args.run_name}")
            mlflow.log_params(hparams.to_dict())
            for epoch in range(1, n_epochs + 1):
                model.train()
                with t.enable_grad():
                    train_losses = []
                    train_outputs = None
                    train_targets = None
                    max_grad = float("-inf")
                    for batch_inputs, batch_targets in traindl:
                        batch_inputs = batch_inputs.to(DEVICE)
                        batch_targets = batch_targets.to(DEVICE)

                        optim.zero_grad()
                        batch_outputs = model.forward(batch_inputs)
                        loss = loss_fn(batch_outputs, batch_targets)
                        loss.backward()
                        # t.nn.utils.clip_grad_value_(model.parameters(), hparams.clip)
                        for param in model.parameters():
                            if t.max(param.grad) > max_grad:
                                max_grad = t.max(param.grad)
                        optim.step()

                        train_losses.append(loss.detach().item())
                        if train_outputs is not None:
                            train_outputs = np.concatenate(
                                (train_outputs, batch_outputs.detach().cpu().numpy()), axis=0
                            )
                            train_targets = np.concatenate(
                                (train_targets, batch_targets.detach().cpu().numpy()), axis=0
                            )
                        else:
                            train_outputs = batch_outputs.detach().cpu().numpy()
                            train_targets = batch_targets.detach().cpu().numpy()

                if max_grad > args.grad_warning_threshold:
                    logging.warning(f"Epoch {epoch} Gradients {max_grad:.3f} are too high!")
                train_loss = np.around(np.mean(train_losses), 3)
                if train_loss > args.loss_warning_threshold:
                    logging.warning(f"Epoch {epoch}: Training loss {train_loss:.3f} is too high!")

                mlflow.log_metric("train_loss", train_loss, step=epoch)
                for metric in self._metrics:
                    mval = np.around(metric(train_outputs, train_targets), 3)
                    mlflow.log_metric(f"train_{metric.__name__}", mval, step=epoch)

                model.eval()
                with t.no_grad():
                    val_losses = []
                    val_outputs = None
                    val_targets = None
                    for batch_inputs, batch_targets in valdl:
                        batch_inputs = batch_inputs.to(DEVICE)
                        batch_targets = batch_targets.to(DEVICE)
                        batch_outputs = model(batch_inputs)
                        loss = loss_fn(batch_outputs, batch_targets)

                        val_losses.append(loss.detach().item())
                        if val_outputs is not None:
                            val_outputs = np.concatenate(
                                (val_outputs, batch_outputs.detach().cpu().numpy())
                            )
                            val_targets = np.concatenate(
                                (val_targets, batch_targets.detach().cpu().numpy())
                            )
                        else:
                            val_outputs = batch_outputs.detach().cpu().numpy()
                            val_targets = batch_targets.detach().cpu().numpy()

                val_loss = np.around(np.mean(val_losses), 3)
                mlflow.log_metric("val_loss", val_loss, step=epoch)
                for metric in self._metrics:
                    mval = np.around(metric(val_outputs, val_targets), 3)
                    mlflow.log_metric(f"val_{metric.__name__}", mval, step=epoch)

                if epoch % self.log_frequency == 0:
                    logging.info(
                        f"Epoch {epoch}: Train loss={train_loss:.3f} Val loss={val_loss:.3f}"
                    )

            model.eval()
            with t.no_grad():
                val_losses = []
                val_outputs = None
                val_targets = None
                for batch_inputs, batch_targets in valdl:
                    batch_inputs = batch_inputs.to(DEVICE)
                    batch_targets = batch_targets.to(DEVICE)
                    batch_outputs = model(batch_inputs)
                    loss = loss_fn(batch_outputs, batch_targets)

                    val_losses.append(loss.detach().item())
                    if val_outputs is not None:
                        val_outputs = np.concatenate(
                            (val_outputs, batch_outputs.detach().cpu().numpy())
                        )
                        val_targets = np.concatenate(
                            (val_targets, batch_targets.detach().cpu().numpy())
                        )
                    else:
                        val_outputs = batch_outputs.detach().cpu().numpy()
                        val_targets = batch_targets.detach().cpu().numpy()
            val_loss = np.around(np.mean(val_losses), 3)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            for metric in self._metrics:
                mval = metric(val_outputs, val_targets)
                mlflow.log_metric(f"val_{metric.__name__}", np.around(mval, 3), step=n_epochs)
                self.final_val_metrics.append(mval)

            if save_model:
                mlflow.pytorch.log_model(model, "model")
            self.model = model
            self.model_path = run.info.artifact_uri + "/model"
