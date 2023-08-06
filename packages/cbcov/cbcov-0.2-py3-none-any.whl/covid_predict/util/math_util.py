import numpy as np
import torch


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


def RalstonIntegrator():
    def subf1(x, xdot, dt):
        return tuple(map(lambda x, xdot: x + (2 * dt / 3) * xdot, x, xdot))

    def subf2(x, xdot, xdoti, dt):
        return tuple(map(lambda x, xdot, xdoti:
                         x + (.25 * dt) * (xdot + 3 * xdoti), x, xdot, xdoti))

    def f(ODESystem, x0, nt, deltat=1.0):
        if torch.is_tensor(x0[0]):
            x = tuple(map(lambda x: x.clone(), x0))
        else:
            x = x0
        if nt > 0:
            dt = deltat / nt
        l = [x]
        for i in range(nt):
            xdot = ODESystem(*x)
            xi = subf1(x, xdot, dt)
            # xi = tuple(map(lambda x, xdot: x + (2 * dt / 3) * xdot, x, xdot))
            xdoti = ODESystem(*xi)
            x = subf2(x, xdot, xdoti, dt)
            # x = tuple(map(lambda x, xdot,
            #  ....xdoti: x + (.25 * dt) * (xdot + 3 * xdoti), x, xdot, xdoti))
            l.append(x)
        return l

    return f
