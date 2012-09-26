import readDigits, predict

import numpy as np

X,y = readDigits.loadSet('digits.jpg', 10, 5, "72104149590690159734966540740131347271211792351244")

print len(y)

labels = y.max()+1

m, n = X.shape

theta = np.zeros((labels, n + 1))
X = np.hstack([np.ones((m, 1)), X])

initial_t = np.zeros((n + 1, 1))

J, grad= predict.lrCost(initial_t, X, y, 0.1)

print J.shape, J

print grad.shape, grad

