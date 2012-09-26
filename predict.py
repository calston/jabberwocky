import numpy as np

def sigmoid(z):
    # Sigmoid function 
    return 1.0 / (1 + np.exp(-z))


def minimiseLRF(X, y, l):
    # Minimuses logistic sigmoid function to theta
    labels = y.max()+1
    
    m, n = X.shape

    theta = np.zeroes((lables, n + 1))
    X = np.hstack([np.ones((m, 1)), X])

    for i in range(labels):
        
