from dataclasses import dataclass
import torch as t
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchutils.core.trainer import Trainer, TrainerArgs
from torchutils.core.evaluator import evaluate
from torchutils.metrics import rmse
from torchutils.core.hyperparams import Hyperparams
import mlflow
import os.path as path
import logging

logformat = "[%(levelname)s %(asctime)s] %(process)s-%(name)s: %(message)s"
logging.basicConfig(format=logformat, datefmt="%m-%d %I:%M:%S", level=logging.DEBUG)
logging.getLogger("git.cmd").setLevel(logging.ERROR)

mlflow.set_tracking_uri(path.expanduser("~/mlruns"))


class RegressionDS(Dataset):
    def __init__(self):
        # Lets pretend we 10 features and a 100 instances so 100 x 10 (m x n)
        self._x = np.random.standard_normal((100, 10)).astype(np.float32)
        self._y = np.random.random(100).astype(np.float32)

    def __len__(self):
        return 100

    def __getitem__(self, idx):
        return self._x[idx], self._y[idx]


class SimpleLR(t.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = t.nn.Linear(10, 1)

    def forward(self, batch_x):
        batch_y = self.fc(batch_x)
        return batch_y.squeeze(dim=1)


@dataclass
class DummyHparams(Hyperparams):
    batch_size: int


def build_trainer(hparams, trainset, valset):
    run_name = "tbd_run" + str(np.random.randint(10, 10_000))
    model = SimpleLR()
    optim = t.optim.Adam(model.parameters())
    loss_fn = t.nn.MSELoss(reduction="mean")
    traindl = DataLoader(trainset, batch_size=hparams.batch_size)
    valdl = DataLoader(valset, batch_size=hparams.batch_size)
    return TrainerArgs(
        run_name=run_name,
        model=model,
        optim=optim,
        loss_fn=loss_fn,
        trainloader=traindl,
        valloader=valdl,
        n_epochs=3,
    )


def test_train_eval(batch_size):
    trainset = RegressionDS()
    valset = RegressionDS()
    trainer = Trainer("TBDExp", trainset, valset, metrics=[rmse])
    trainer.log_frequency = 1
    hparams = DummyHparams(batch_size=batch_size)
    trainer.train(hparams, build_trainer)

    dl = DataLoader(trainset, batch_size=batch_size)
    evaluate(trainer.model, dl, [rmse])


def test_even_batches():
    test_train_eval(10)


def test_small_last_batch():
    test_train_eval(6)


def test_single_trailing_batch():
    test_train_eval(9)


if __name__ == "__main__":
    test_even_batches()
    test_small_last_batch()
    test_single_trailing_batch()
