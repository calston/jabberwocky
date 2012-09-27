import numpy as np
from scipy import optimize


def sigmoid(z):
    # Sigmoid function 
    return 1.0 / (1 + np.exp(-z))

def lrCost(theta, X, y, l):
    # Logistic regression cost function
    rTheta = theta.copy()
    rTheta[0] = 0

    m = float(len(y))

    hx = sigmoid(X.dot(theta))

    J = (1.0/m) * (-y.dot(np.log(hx)) - (1.0 - y).dot(np.log(1.0 - hx))) + (l/(2.0*m))*(rTheta**2).sum()

    return J

def lrGrad(theta, X, y, l):
    # Logistic regression gradient function
    rTheta = theta.copy()
    rTheta[0] = 0

    m = float(len(y))

    hx = sigmoid(X.dot(theta))


    grad = 1.0/m * (hx - y).dot(X) + (l/m)*rTheta

    return grad.transpose()
   

def minimiseLRF(X, y, l):
    # Minimuses logistic sigmoid function to theta for each discrete set
    labels = y.max()+1
    
    m, n = X.shape

    theta = np.zeros((labels, n + 1))
    X = np.hstack([np.ones((m, 1)), X])

    for i in range(labels):
        initial_t = np.zeros((n + 1, 1)).transpose()

        tset = 0+(y==i)
        lrC = lambda t: lrCost(t, X, tset, 0.1)
        lrG = lambda t: lrGrad(t, X, tset, 0.1) 
        
        qtheta = optimize.fmin_cg(lrC, initial_t, lrG, maxiter=100)

        theta[i, :] = qtheta
        
    print theta
    return theta

def predict(system, theta):
    X = np.hstack([[1], system])

    print "~~", theta.dot(X)

    r = sigmoid(theta.dot(X));

    print r
    print r>0.5

    print max(r)

    return r.argmax()

