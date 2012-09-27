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


print "Starting..."
X,y = readDigits.loadSet('samples/digits.jpg', 10, 5, "72104149590690159734966540740131347271211792351244")

X2,y2 = readDigits.loadSet('samples/moredigits.png', 10, 9, "111111111112222222223333333333444444444455555555556666666666777777777788888888889999999999")

X = np.vstack([X, X2])
y = np.hstack([y, y2])

print "Training logistic analyser"
theta = predict.minimiseLRF(X, y, 0.1)


print "Picking a test"
blocks = readDigits.isolateDigits('samples/sample1.png')
myBlock = blocks[6]
blockVector = np.asarray(myBlock)#.flatten()
print blockVector

val = predict.predict(blockVector.flatten(), theta)

print "The digit looks like ", val

