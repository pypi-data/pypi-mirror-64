import numpy as np


def accuracy(outputs, targets):
    """
    Computes the fraction of predictions that match the targets.

    Args:
        outputs (ndarray): This is a 2D numpy array of shape m x k where m is the mini-batch size
        and k is the number of classes. The exact values of m and k do not matter. What matters is
        that this is a 2D array. The elements of this matrix can be logits or probabilities.

        targets (ndarray): This is a 1D numpy array of length m.

    Returns:
        float: The fraction of predictions that match the targets.
    """
    if outputs.shape[0] != targets.shape[0]:
        raise ValueError(
            f"outputs shape {outputs.shape[0]} and targets shape {targets.shape[0]} must be equal!"
        )
    predictions = np.argmax(outputs, axis=1)
    correct = np.sum(predictions == targets)
    return correct / targets.shape[0]


def rmse(outputs, targets):
    """
    Computes the Root Mean Square Error between outputs and targets.

    Args:
        outputs (ndarray): A 1D array of floats.
        targets (ndarray): A 1D array of floats of the same length as outputs.

    Returns:
        float: The RMSE.
    """
    if outputs.shape[0] != targets.shape[0]:
        raise ValueError(
            f"outputs shape {outputs.shape[0]} and targets shape {targets.shape[0]} must be equal!"
        )
    mse = np.mean(np.power((outputs - targets), 2))
    return np.sqrt(mse)


def mae(outputs, targets):
    """
    Computes Mean Absolute Error between the outputs and target.

    Args:
        outputs (ndarray): A 1D array of floats.
        targets (ndarray): A 1D array of floats.

    Returns:
        float: The MAE.
    """
    if outputs.shape[0] != targets.shape[0]:
        raise ValueError(
            f"outputs shape {outputs.shape[0]} does not match the targets shape {targets.shape[0]}!"
        )
    return np.mean(np.abs(outputs - targets))
