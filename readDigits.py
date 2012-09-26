from PIL import Image, ImageOps
from matplotlib import pyplot
import numpy

def readImage(filename, w, h):
    im = ImageOps.invert(Image.open(filename)).convert('L')

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
                (x, y, x+blX, y+blY)).resize((20, 20))

            blocks.append(
                numpy.asarray(imBlock.convert('L')).flatten()
            )
    
    return numpy.vstack(blocks)

def loadSet(filename, w, h, vals):
    X = readImage(filename, w, h)

    return X, numpy.array([int(i) for i in vals])


