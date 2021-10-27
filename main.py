import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt 

debug = True

if debug :
    print("[DEBUG] Chargement de l'image requete...")

def computeHistoVector (inputImage) :

    rHisto = cv.calcHist([inputImage], [0], None, [256], [0, 256])
    gHisto = cv.calcHist([inputImage], [1], None, [256], [0, 256])
    bHisto = cv.calcHist([inputImage], [2], None, [256], [0, 256])

    rHisto = rHisto.flatten()
    gHisto = gHisto.flatten()
    bHisto = bHisto.flatten()

    rHisto = cv.normalize(rHisto, rHisto)
    gHisto = cv.normalize(gHisto, gHisto)
    bHisto = cv.normalize(bHisto, bHisto)

    histo = np.concatenate((rHisto, gHisto, bHisto))

    return histo

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
    
    histoQuery = computeHistoVector(queryImg)

if debug : 
    if histoQuery is not None and histoQuery.shape == (768,) :
        print("[DEBUG] Vecteur carateristique de la requete calculé (shape OK)")
    else : 
        print("[DEBUG] Echec du calcul du vecteur caractéristique de la requete")
        print("[DEBUG] Sorti du programme...")
        exit()
