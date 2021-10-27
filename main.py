import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt 

debug = True

if debug :
    print("[DEBUG] Chargement de l'image")

try : 
    queryImg = cv.imread('./data/small/queries/152029243_b3582c36fa.jpg', cv.IMREAD_COLOR)
except ValueError:
    print("[DEBUG] Echec du chargement de l'image")

if debug and queryImg is None :
    print("[DEBUG] Echec du chargement de l'image")
    exit()
elif debug and queryImg.all() != None :
    print("[DEBUG] Image chargée avec succés")

rHistoQuery = cv.calcHist([queryImg], [0], None, [256], [0, 256])
gHistoQuery = cv.calcHist([queryImg], [1], None, [256], [0, 256])
bHistoQuery = cv.calcHist([queryImg], [2], None, [256], [0, 256])

rHistoQuery = rHistoQuery.flatten()
gHistoQuery = gHistoQuery.flatten()
bHistoQuery = bHistoQuery.flatten()

rHistoQuery = cv.normalize(rHistoQuery, rHistoQuery)
gHistoQuery = cv.normalize(gHistoQuery, gHistoQuery)
bHistoQuery = cv.normalize(bHistoQuery, bHistoQuery)

histoQuery = np.concatenate((rHistoQuery, gHistoQuery, bHistoQuery))