from typing import Callable, Sequence

import numpy as np
import torch as t
from torch.utils.data import DataLoader

MetricFunc = Callable[[Sequence[float], Sequence[float]], float]
DEVICE = t.device("cuda" if t.cuda.is_available() else "cpu")


def evaluate(model: t.nn.Module, dataloader: DataLoader, metrics: Sequence[MetricFunc]):
    model = model.to(DEVICE)
    model.eval()
    with t.no_grad():
        outputs = None
        targets = None
        for batch_inputs, batch_targets in dataloader:
            batch_inputs = batch_inputs.to(DEVICE)
            batch_targets = batch_targets.to(DEVICE)
            batch_outputs = model(batch_inputs)
            if outputs is not None:
                outputs = np.concatenate((outputs, batch_outputs.detach().cpu().numpy()))
                targets = np.concatenate((targets, batch_targets.detach().cpu().numpy()))
            else:
                outputs = batch_outputs.detach().cpu().numpy()
                targets = batch_targets.detach().cpu().numpy()
    mvals = []
    for metric in metrics:
        mval = np.around(metric(outputs, targets), 3)
        mvals.append(mval)
    return mvals
