import logging
import os.path as path
from collections import OrderedDict
from dataclasses import dataclass

import mlflow
import torch as t
import torchvision as tv
from haikunator import Haikunator
from torch.utils.data import DataLoader

import torchutils as tu
from torchutils.metrics import accuracy

DATAROOT = path.expanduser("~/mldata/pytorch")
mlflow.set_tracking_uri(path.expanduser("~/mlruns"))

logformat = "[%(levelname)s %(asctime)s] %(process)s-%(name)s: %(message)s"
logging.basicConfig(format=logformat, datefmt="%m-%d %I:%M:%S", level=logging.DEBUG)
logging.getLogger("git.cmd").setLevel(logging.ERROR)


def prep_datasets():
    xform = tv.transforms.Compose(
        [tv.transforms.ToTensor(), tv.transforms.Normalize((0.5,), (0.5,))]
    )

    datapath = path.join(DATAROOT, "fashion-mnist")
    train_val_set = tv.datasets.FashionMNIST(datapath, download=True, train=True, transform=xform)
    train_size = int(len(train_val_set) * 0.8)
    val_size = len(train_val_set) - train_size
    trainset, valset = t.utils.data.random_split(train_val_set, [train_size, val_size])
    testset = tv.datasets.FashionMNIST(datapath, download=True, train=False, transform=xform)
    return trainset, valset, testset


@dataclass
class MyHyperparams(tu.Hyperparams):
    batch_size: int
    n_epochs: int
    lr: float


def create_model():
    model = t.nn.Sequential(
        OrderedDict(
            [
                ("flatten", t.nn.Flatten()),
                ("fc1", t.nn.Linear(784, 128)),
                ("relu1", t.nn.ReLU()),
                ("fc2", t.nn.Linear(128, 64)),
                ("relu2", t.nn.ReLU()),
                ("fc3", t.nn.Linear(64, 32)),
                ("relu3", t.nn.ReLU()),
                ("logits", t.nn.Linear(32, 10)),
            ]
        )
    )
    return model


def build_trainer(hparams, trainset, valset):
    run_name = Haikunator().haikunate()
    model = create_model()
    optim = t.optim.SGD(model.parameters(), lr=hparams.lr)
    loss_fn = t.nn.CrossEntropyLoss()
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
    hparams = MyHyperparams(batch_size=32, n_epochs=3, lr=0.25)
    model, model_path = tu.train(
        "FashionMNIST", trainset, valset, [accuracy], hparams, build_trainer
    )
    print(f"Model saved at {model_path}")

    # Alternately I can load the model from disk
    # model = mlflow.pytorch.load_model(trainer.model_path)
    testdl = DataLoader(testset, batch_size=5000)
    acc = tu.evaluate(model, testdl, [accuracy])[0]
    print(f"Test accuracy: {acc:.3f}")


def tune():
    trainset, valset, testset = prep_datasets()

    hparams_spec = tu.HyperparamsSpec(
        factory=MyHyperparams,
        spec=[
            {"name": "batch_size", "type": "choice", "value_type": "int", "values": [16, 32, 64]},
            {"name": "n_epochs", "type": "range", "value_type": "int", "bounds": [2, 5]},
            {"name": "lr", "type": "range", "bounds": [1e-6, 0.4], "log_scale": True},
        ],
    )
    best_model, best_model_path = tu.autotune(
        "TuneFashionMNIST", trainset, valset, accuracy, hparams_spec, build_trainer, total_trials=3
    )
    print(f"Best model saved at {best_model_path}")

    # Alternately I can load the model from disk
    # model = mlflow.pytorch.load_model(tuner.best_model_path)
    testdl = DataLoader(testset, batch_size=5000)
    acc = tu.evaluate(best_model, testdl, [accuracy])[0]
    print(f"Test accuracy: {acc:.3f}")


if __name__ == "__main__":
    # single()
    tune()
