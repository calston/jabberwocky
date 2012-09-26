import readDigits, predict

import numpy as np

def test1():

    X = np.array([
        [1, 2, 3, 3], 
        [1, 2, 3, 4], 
        [1, 2, 4, 5], 
        [1, 2, 5, 5]
    ])

    y = np.array([1, 1, 2, 2]).transpose()

    initial_t = np.array([0.5, 0.5, 0.5, 0.5]).transpose()

    print X
    print y, initial_t

    J= predict.lrCost(initial_t, X, y, 0.1)

    print J.shape, J

X,y = readDigits.loadSet('digits.jpg', 10, 5, "72104149590690159734966540740131347271211792351244")

predict.minimiseLRF(X, y, 0.1)
