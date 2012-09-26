import numpy as np

def sigmoid(z):
    # Sigmoid function 
    return 1.0 / (1 + np.exp(-z))

def lrCost(theta, X, y, l):
    # Logistic regression cost function
    rTheta = theta
    rTheta[0] = 0
    m = len(y)

    hx = sigmoid(X.dot(theta));

    return 1/m * (-y.transpose()*np.log(hx) - (1 - y.transpose())*np.log(1 - hx)) + (l/(2*m))*(rTheta**2).sum()

def minimiseLRF(X, y, l):
    # Minimuses logistic sigmoid function to theta for each discrete set
    labels = y.max()+1
    
    m, n = X.shape

    theta = np.zeros((labels, n + 1))
    X = np.hstack([np.ones((m, 1)), X])

    for i in range(labels):
        initial_t = np.zeros((n + 1, 1))
        
        lcJ = lambda t: lrCost(t, X, y, 0.1)

        # ... where's my minimizorz :( 
        optimize.fmin_cg(lcJ, initial_t, maxiter=100)
