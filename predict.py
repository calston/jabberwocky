import numpy as np
from scipy import optimize


def sigmoid(z):
    # Sigmoid function 
    return 1.0 / (1 + np.exp(-z))

def lrCost(theta, X, y, l):
    # Logistic regression cost function
    rTheta = theta.copy()
    rTheta[0] = 0

    m = len(y)

    hx = sigmoid(X.dot(theta))

    J = 1.0/m * (-y.dot(np.log(hx)) - (1 - y).dot(np.log(1 - hx))) + (l/(2*m))*(rTheta**2).sum()

    return J

def lrGrad(theta, X, y, l):
    # Logistic regression gradient function
    rTheta = theta.copy()
    rTheta[0] = 0

    m = len(y)

    hx = sigmoid(X.dot(theta))


    grad = 1.0/m * (hx - y).dot(X) + (l/m)*rTheta
    
    return grad
   

def minimiseLRF(X, y, l):
    # Minimuses logistic sigmoid function to theta for each discrete set
    labels = y.max()+1
    labels = 1
    
    m, n = X.shape

    theta = np.zeros((labels, n + 1))
    X = np.hstack([np.ones((m, 1)), X])

    for i in range(labels):
        initial_t = np.zeros((n + 1, 1))

        lrC = lambda t: lrCost(t, X, y, 0.2)
        lrG = lambda t: lrGrad(t, X, y, 0.2) 
        
        q = optimize.fmin_cg(lrC, initial_t, lrG, maxiter=40)

        print q[0], q[1]

