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
    g= predict.lrGrad(initial_t, X, y, 0.1)

    print J
    print g


X,y = readDigits.loadSet('digits.jpg', 10, 5, "72104149590690159734966540740131347271211792351244")

# This set is too small, only 50 samples - we need that to be many times more

print "Starting..."

nx1 = X.copy()
ny1 = y.copy()

print nx1.shape, ny1.shape

for i in []: #range(99):
    X = np.vstack([X, nx1])
    y = np.hstack([y, ny1])

print X.shape, y.shape

predict.minimiseLRF(X, y, 0.1)
