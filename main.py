import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt 

img = cv.imread('./data/small/images/10815824_2997e03d76.jpg', cv.IMREAD_COLOR)

rHisto = cv.calcHist([img], [0], None, [256], [0, 256])
gHisto = cv.calcHist([img], [1], None, [256], [0, 256])
bHisto = cv.calcHist([img], [2], None, [256], [0, 256])

rHisto = rHisto.flatten()
gHisto = gHisto.flatten()
bHisto = bHisto.flatten()

rHisto = cv.normalize(rHisto, rHisto)
gHisto = cv.normalize(gHisto, gHisto)
bHisto = cv.normalize(bHisto, bHisto)

plt.plot(rHisto, color="r")
plt.plot(gHisto, color="g")
plt.plot(bHisto, color="b")
plt.xlim([0,256])
plt.show()

histo = np.concatenate((rHisto, gHisto, bHisto))
