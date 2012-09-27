from PIL import Image, ImageOps
from matplotlib import pyplot
import numpy

BLOCKSIZE = 16

def readImage(filename, w, h):
    """ Loads an image and cuts it up based on a grid """
    im = ImageOps.invert(Image.open(filename).convert('L'))

    x, y = im.size

    blY = y/h
    blX = x/w

    # Create blocks
    blocks = []
    for i in range(h):  
        for j in range(w):
            x, y = (j*blX, i*blY) 

            # Get a block from the sample and resize 
            imBlock = im.crop(
                (x, y, x+blX, y+blY)).resize((BLOCKSIZE, BLOCKSIZE))

            blocks.append(
                numpy.asarray(imBlock).flatten()
            )

    return numpy.vstack(blocks)

def loadSet(filename, w, h, vals):
    """ Load a set with a grid and values """
    X = readImage(filename, w, h)

    return X, numpy.array([int(i) for i in vals])


