import numpy as np

class GameError(Exception):
    ...

def sampleboard():
    res = np.array([
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [0, 1, 1, 1],
    ])
    return res


def samplepiece():
    res = np.array([
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 0, 0],
    ])
    return res

