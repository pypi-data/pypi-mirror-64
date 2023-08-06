from typing import Sequence

from torch.utils.data import Dataset

from .core.auto_tuner import AutoTuner
from .core.hyperparams import Hyperparams, HyperparamsSpec
from .core.trainer import ArgsBuilderType, MetricFunc, Trainer


def train(
    exp_name: str,
    trainset: Dataset,
    valset: Dataset,
    metrics: Sequence[MetricFunc],
    hparams: Hyperparams,
    args_builder: ArgsBuilderType,
    log_frequency: int = 10,
):
    trainer = Trainer(exp_name, trainset, valset, metrics)
    trainer.log_frequency = log_frequency
    trainer.train(hparams, args_builder)
    return trainer.model, trainer.model_path, trainer.final_val_metrics


def autotune(
    exp_name: str,
    trainset: Dataset,
    valset: Dataset,
    obj_metric: MetricFunc,
    hparams_spec: HyperparamsSpec,
    args_builder: ArgsBuilderType,
    total_trials=20,
):
    tuner = AutoTuner(exp_name, trainset, valset, obj_metric)
    tuner.tune(hparams_spec, args_builder, total_trials)
    return tuner.best_model, tuner.best_model_path
