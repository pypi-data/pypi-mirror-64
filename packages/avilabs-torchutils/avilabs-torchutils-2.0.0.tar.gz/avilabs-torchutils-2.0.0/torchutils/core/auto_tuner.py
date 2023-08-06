import logging
from typing import Callable, Sequence

from ax.service.managed_loop import optimize
from torch.utils.data import Dataset

from .hyperparams import HyperparamsSpec
from .trainer import ArgsBuilderType, Trainer

MetricFunc = Callable[[Sequence[float], Sequence[float]], float]


class AutoTuner:
    def __init__(
        self,
        exp_name: str,
        trainset: Dataset,
        valset: Dataset,
        obj_metric: MetricFunc,
        minimize=False,
    ):
        self._trainer = Trainer(exp_name, trainset, valset, [obj_metric])
        self._trainer.log_frequency = 10_000
        self._obj_metric = obj_metric
        self._minimize = minimize
        self._hparams_factory = None
        self._args_builder = None
        self.metric_values = []

    def _train_eval(self, hparams):
        hparams = self._hparams_factory(**hparams)
        self._trainer.train(hparams, self._args_builder, save_model=False)
        self.metric_values.append(self._trainer.final_val_metrics[0])
        return {self._obj_metric.__name__: (self._trainer.final_val_metrics[0], 0.0)}

    def tune(self, hparams_spec: HyperparamsSpec, args_builder: ArgsBuilderType, total_trials=20):
        self._hparams_factory = hparams_spec.factory
        self._args_builder = args_builder

        best_params, values, _, _ = optimize(
            hparams_spec.spec,
            evaluation_function=self._train_eval,
            objective_name=self._obj_metric.__name__,
            total_trials=total_trials,
            minimize=self._minimize,
        )

        logging.info(f"best_params={best_params} values={values}")
        self._trainer.log_frequency = 1
        hparams = self._hparams_factory(**best_params)
        self._trainer.train(hparams, args_builder)
        self.best_model = self._trainer.model
        self.best_model_path = self._trainer.model_path
