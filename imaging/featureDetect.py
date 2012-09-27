from PIL import Image, ImageOps, ImageDraw, ImageFont
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


def findParent(x, y, features):
    # Find aproximately neighboring pixels in the features set
    # and return the parents of those neighbors
    found = []
    for i in range(-2,3):
        for j in range(-2,3):
            # Run through every permutation of the nearest nodes
            tpl = (x+i, y+j)
            # Return the parent for the neighbor node
            f = features.get(tpl, None)
            if f and (f not in found):
                found.append(f)
    return found

def isolateDigits(filename, contrastMin=100, contrastMax=256, tollerance=20, correctionFactor = 5, showTest = False):
    """Isolates and extracts features from an image.
            
            The image is reduced to scan lines. On each line points are
            found in the intensity range from contrastMin to contrastMax. 
            For each new point found, a map of connected points is created 
            back to the first parent in the feature 
                point => parent(neighbor)
            The parent is also mapped back to child points
                parent => [c1, c2, ..., cn]
            If a point is found to have multiple neighbors which 
            resolve to multiple parents, the first parent chosen 
            to replace all other parents thus merging the tree for that feature.
            (the parent=>child reverse map speeds this up) 
            Once the image is scanned, the map is reversed creating new map
            of parents to sets of X and Y values the children occupied
            The minima and maxima of these sets define the bounding box of the 
            feature. 

        tollerance - The minimum area something must be bound by to be 
                     considered a feature
        correctionFactor - Additional area around the feature bounding
        showTest - Display some useful test imagary of what happened
    """
    im = ImageOps.invert(Image.open(filename)).convert('L')
    w, h = im.size
    x, y = (0,1)

    # Our set of feature indexes
    features = {}
    # Children of feature parents
    pchildren = {}

    # Scan image sequentially
    st = im.getdata()
    for val in st:
        x+= 1
        # Find bright pixels
        point = (val >= contrastMin) and (val <= contrastMax)

        if point:
            # Find neighboring pixels
            feature = findParent(x,y, features)
            if feature:
                # Index the parent feature to this feature tree
                if len(feature) > 1:
                    # Merge these trees together
                    rparent = feature[0]
                    for f in feature[1:]:
                        for child in pchildren[f]:
                            features[child] = rparent
                            pchildren[rparent].append(child)
                        pchildren[f] = []
                else:
                    features[(x,y)] = feature[0]
                    pchildren[feature[0]].append((x,y))
            else:
                features[(x,y)] = (x,y)
                pchildren[(x,y)] = []
        
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

        # Discard noise
        area = (x2-x1)*(y2-y1)
        if area > tollerance:
            features.append((
                x1-correctionFactor, y1-correctionFactor, 
                x2+correctionFactor, y2+correctionFactor))

    features.sort(key = lambda k: (k[1], k[0]))

    # Cut all the features out of the primary image and resize
    blocks = []
    for box in features:
        imBlock = im.crop(
            (box[0]-2, box[1]-2, box[2]+2, box[3]+2)
        ).resize((BLOCKSIZE, BLOCKSIZE))
        blocks.append(imBlock)

    # Display the test image
    if showTest:
        im = im.convert('RGB')
        draw = ImageDraw.Draw(im)
        boxnum = 0
        for box in features:
            boxnum += 1
            x1, y1, x2, y2 = box
            draw.rectangle(
                (x1-2, y1-2, x2+2, y2+2),
            outline="#ff0000")
            
            draw.text((x1 + (x2-x1)/2, y1 + (y2-y1)/2), str(boxnum), fill="#00ff00")

        im.show()

    return blocks