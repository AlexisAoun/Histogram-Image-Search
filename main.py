import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt 

debug = True

if debug :
    print("[DEBUG] Chargement de l'image requete...")

try : 
    queryImg = cv.imread('./data/small/queries/152029243_b3582c36fa.jpg', cv.IMREAD_COLOR)
except ValueError:
    print("[DEBUG] Echec du chargement de l'image requete")
    print("[DEBUG] Sorti du programme...")
    exit()

if debug and queryImg is None :
    print("[DEBUG] Echec du chargement de l'image requete")
    print("[DEBUG] Sorti du programme...")
    exit()
elif debug and queryImg.all() != None :
    print("[DEBUG] Image requete chargée avec succés")

if debug :
    print("[DEBUG] Calcule du vecteur carateristique de la requete...")
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

print(histoQuery.shape)
if debug and histoQuery is not None and histoQuery.shape == (768,):
    print("[DEBUG] Vecteur carateristique de la requete calculé (shape OK)")