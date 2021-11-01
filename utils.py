import cv2 as cv
import numpy as np


# fonction qui calcule le vector histographique d une image passee en parametre
def computeHistoVector(inputImage):

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


# fonctionne qui retourne une image dont le path est passe en parametre
def getImage(path, debug):

    try:

        img = cv.imread(path, cv.IMREAD_COLOR)

    except ValueError:

        print("[DEBUG] Echec du chargement de l'image")
        print("[DEBUG] Sortie du programme...")
        exit()

    if debug and img is None:

        print("[DEBUG] Echec du chargement de l'image")
        print("[DEBUG] Sortie du programme...")
        exit()

    elif debug and img.all() != None:

        print("[DEBUG] Image chargee avec succes")

    return img
