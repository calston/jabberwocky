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

def snapTo(x, y, features):
    # Find aproximately neighbouring pixels in the features set
    for i in range(-2,3):
        for j in range(-2,3):
            # Run through every permutation of the nearest nodes
            tpl = (x+i, y+j)
            if tpl in features:
                return tpl
    return None

def isolateDigits(filename):
    """ A very very suboptimal quick and dirty feature detection
        using scanlines and a tree and some solidly unfounded 
        principals """

    im = ImageOps.invert(Image.open(filename)).convert('L')
    w, h = im.size
    x, y = (0,1)

    feature_index = 0
    features = {}

    st = im.getdata()
    for val in st:
        x+= 1

        # Find bright pixels
        point = val > 80

        if point:
            # Find neighbouring pixels
            feature = snapTo(x,y, features)
            if feature:
                # Index the parent feature to this feature
                ft = features[feature]
            else:
                ft = (x, y)

            features[(x,y)] = ft
        
        # Reset the scan line
        if x == w:
            y += 1 
            x = 0

    # Reverse the feature set, aggregating it down to the parent feature
    revFeatures = {}
    for k,v in features.items():
        if v in revFeatures:
            # Create a list of x and y points in this feature
            revFeatures[v][0].append(k[0])
            revFeatures[v][1].append(k[1])
        else:
            revFeatures[v] = [
                [k[0]], 
                [k[1]]
            ]

    features = []
    # Create boxes
    for k,v in revFeatures.items():
        x,y = v 
        # Map a box to the extents of the feature
        x1, x2 = (min(x),  max(x))
        y1, y2 = (min(y), max(y))

        # Calculate the feature area to discard any noise
        area = (x2-x1)*(y2-y1)
        if area>600:
            features.append((x1-5, y1-5, x2+5, y2+5))

    # Cut all the features out of the primary image and resize
    blocks = []
    for box in features:
        imBlock = im.crop(
            box).resize((BLOCKSIZE, BLOCKSIZE))
        blocks.append(imBlock)

    return blocks
