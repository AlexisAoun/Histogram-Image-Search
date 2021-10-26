import cv2 as cv
import numpy as np

img = cv.imread(
    'C:/Users/doria/Documents/IMT/M1/ProjetRecherche/images/10815824_2997e03d76.jpg', cv.IMREAD_COLOR)

rHisto = cv.calcHist([img], [0], None, [256], [0, 256])
gHisto = cv.calcHist([img], [1], None, [256], [0, 256])
bHisto = cv.calcHist([img], [2], None, [256], [0, 256])

rHisto = rHisto.flatten()
gHisto = gHisto.flatten()
bHisto = bHisto.flatten()

rHisto = cv.normalize(rHisto, rHisto)
gHisto = cv.normalize(gHisto, gHisto)
bHisto = cv.normalize(bHisto, bHisto)

histo = np.concatenate((rHisto, gHisto, bHisto))
