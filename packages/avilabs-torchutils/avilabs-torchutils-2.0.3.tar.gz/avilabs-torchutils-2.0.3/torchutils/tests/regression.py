import logging
import os.path as path
from dataclasses import dataclass

import mlflow
import sklearn.datasets
import torch as t
import torch.nn.functional as F
from haikunator import Haikunator
from torch.utils.data import DataLoader

import torchutils as tu
from torchutils.metrics import rmse

mlflow.set_tracking_uri(path.expanduser("~/mlruns"))

logformat = "[%(levelname)s %(asctime)s] %(process)s-%(name)s: %(message)s"
logging.basicConfig(format=logformat, datefmt="%m-%d %I:%M:%S", level=logging.DEBUG)
logging.getLogger("git.cmd").setLevel(logging.ERROR)


def prep_datasets():
    n_samples = 100_000
    all_X, all_y = sklearn.datasets.make_regression(n_samples=n_samples, n_features=5, noise=0.5)

    train_size = int(n_samples * 0.7)
    val_size = int(n_samples * 0.2)

    train_X = all_X[:train_size]
    train_y = all_y[:train_size]
    trainset = t.utils.data.TensorDataset(
        t.from_numpy(train_X).to(t.float32), t.from_numpy(train_y).to(t.float32)
    )

    val_X = all_X[train_size : train_size + val_size]
    val_y = all_y[train_size : train_size + val_size]
    valset = t.utils.data.TensorDataset(
        t.from_numpy(val_X).to(t.float32), t.from_numpy(val_y).to(t.float32)
    )

    test_X = all_X[train_size + val_size :]
    test_y = all_y[train_size + val_size :]
    testset = t.utils.data.TensorDataset(
        t.from_numpy(test_X).to(t.float32), t.from_numpy(test_y).to(t.float32)
    )

    return trainset, valset, testset


@dataclass
class MyHyperparams(tu.Hyperparams):
    batch_size: int
    n_epochs: int
    lr: float


class SimpleLR(t.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = t.nn.Linear(5, 3)
        self.fc2 = t.nn.Linear(3, 1)

    def forward(self, batch_x):
        x = F.relu(self.fc1(batch_x))
        batch_y_hat = self.fc2(x)
        return t.squeeze(batch_y_hat)


def build_trainer(hparams, trainset, valset):
    run_name = Haikunator().haikunate()
    model = SimpleLR()
    optim = t.optim.Adam(model.parameters(), lr=hparams.lr)
    loss_fn = t.nn.MSELoss(reduction="mean")
    traindl = DataLoader(trainset, batch_size=hparams.batch_size, shuffle=True)
    valdl = DataLoader(valset, batch_size=5000)
    return tu.TrainerArgs(
        run_name=run_name,
        model=model,
        optim=optim,
        loss_fn=loss_fn,
        trainloader=traindl,
        valloader=valdl,
        n_epochs=hparams.n_epochs,
    )


def single():
    trainset, valset, testset = prep_datasets()

    trainer = tu.Trainer("SynthLinReg", trainset, valset, metrics=[rmse])
    trainer.log_frequency = 1

    hparams = MyHyperparams(batch_size=32, n_epochs=5, lr=0.005)
    trainer.train(hparams, build_trainer)
    print(f"Model saved at {trainer.model_path}")

    model = trainer.model
    # Alternately I can load the model from disk
    # model = mlflow.pytorch.load_model(trainer.model_path)
    testdl = DataLoader(testset, batch_size=5000)
    rmse_val = tu.evaluate(model, testdl, [rmse])[0]
    print(f"Test RMSE: {rmse_val:.3f}")


def tune():
    trainset, valset, testset = prep_datasets()

    hparams_spec = tu.HyperparamsSpec(
        factory=MyHyperparams,
        spec=[
            {"name": "batch_size", "type": "choice", "value_type": "int", "values": [16, 32, 64]},
            {"name": "n_epochs", "type": "range", "value_type": "int", "bounds": [7, 13]},
            {"name": "lr", "type": "range", "bounds": [1e-6, 0.4], "log_scale": True},
        ],
    )
    tuner = tu.AutoTuner("TuneSynthLinRegMin", trainset, valset, obj_metric=rmse, minimize=True)
    tuner.tune(hparams_spec, build_trainer, total_trials=3)
    print(f"Best model saved at {tuner.best_model_path}")

    model = tuner.best_model
    # Alternately I can load the model from disk
    # model = mlflow.pytorch.load_model(tuner.best_model_path)
    testdl = DataLoader(testset, batch_size=5000)
    rmse_val = tu.evaluate(model, testdl, [rmse])[0]
    print(f"Test RMSE: {rmse_val:.3f}")


if __name__ == "__main__":
    single()
    # tune()
