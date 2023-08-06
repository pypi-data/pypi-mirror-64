import numpy as np

def movingaverage (values: np.array, window: int) -> np.array:
    """
    Computes a moving average

    :param values: a numpy array of shape (x,)
    :param window: an integer representing the window size
    :return: a numpy array
    """
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

