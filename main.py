import os
from pathlib import Path
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import distance as dist
import lsh as LSH

debug = True
debugPlus = False

queryPath = "./data/small/queries/2090339522_d30d2436f9.jpg"
databasePath = "./data/small/images"
numpyPath = Path("./save.npy")

database = []
i = 0
for entry in os.scandir(databasePath):

    if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():

        database.append(str(entry.path))
        i += 1

databaseSize = i


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


def getImage(path, debug):

    try:

        img = cv.imread(path, cv.IMREAD_COLOR)

    except ValueError:

        print("[DEBUG] Echec du chargement de l'image")
        print("[DEBUG] Sorti du programme...")
        exit()

    if debug and img is None:

        print("[DEBUG] Echec du chargement de l'image")
        print("[DEBUG] Sorti du programme...")
        exit()

    elif debug and img.all() != None:

        print("[DEBUG] Image chargee avec succes")

    return img

# Traitement image base de donnée -------------------------------------------------------------------------

# on verifie si un fichier de sauvegarde numpy est present


if numpyPath.is_file():

    if debug:

        print("[DEBUG] Fichier de sauvegarde numpy detecte")
        print("[DEBUG] Chargement de la sauvegarde numpy...")

    allDataHisto = np.load(str(numpyPath))

    if debug and allDataHisto is not None:

        print("[DEBUG] Sauvegarde numpy chargé avec succes")

    elif debug:

        print("[DEBUG] [ERROR] Echec du chargement de la sauvegarde numpy")

else:

    if debug:

        print("[DEBUG] [WARNING] Aucun fichier de sauvegarde numpy detecte")
        print("[DEBUG] Traitement des images de la base de donnee - Cette operation peut prendre du temps")

    allDataHisto = np.ndarray(shape=(databaseSize, 768))
    i = 0

    for path in database:

        if debugPlus:

            print("[DEBUG] Path actuel : "+path)

        allDataHisto[i] = computeHistoVector(getImage((path), debugPlus))
        i += 1

    if debug:

        print("[DEBUG] Traitement termine")
        print("[DEBUG] Sauvegarde du resultat du traitement...")

    np.save(str(numpyPath), allDataHisto)

    if debug and numpyPath.is_file():

        print("[DEBUG] Sauvegarde numpy termine")

    elif debug:

        print("[DEBUG] [WARING] Echec de la sauvegarde numpy")

# Traitement image requete --------------------------------------------------------------------------------

if debug:

    print("[DEBUG] Chargement de l'image requete...")

queryImg = getImage(str(queryPath), debug)

if debug:

    print("[DEBUG] Calcule du vecteur carateristique de la requete...")

histoQuery = computeHistoVector(queryImg)

if debug:

    if histoQuery is not None and histoQuery.shape == (768,):

        print("[DEBUG] Vecteur carateristique de la requete calcule (shape OK)")

    else:

        print("[DEBUG] Echec du calcul du vecteur caracteristique de la requete")
        print("[DEBUG] Sorti du programme...")
        exit()

# Recherche ---------------------------------------------------------------------------------------------

if debug:
    print("[DEBUG] Calcule Brute knn et radius L2")

resBruteKnnL2 = dist.knn_search(allDataHisto, histoQuery, k=3)
resBruteRadiusL2 = dist.radius_search(allDataHisto, histoQuery, r=1)

print("Image requete : "+str(queryPath))

print("Brute force knn L2")

for i in range(len(resBruteKnnL2[0])):

    print("- Resultat "+str(i)+" : " +
          str(database[resBruteKnnL2[0][i]])+" distance : "+str(resBruteKnnL2[1][i]))

print("")
print("Brute force radius L2")
for i in range(len(resBruteRadiusL2[0])):

    print("- Resultat "+str(i)+" : " +
          str(database[resBruteRadiusL2[0][i]])+" distance : "+str(resBruteRadiusL2[1][i]))

w = 1
nbProjections = 2
nbTabHash = 1

print("")
print("Recherche LSH : W = "+str(w)+" nb projections : "+str(nbProjections))

lsh = LSH.LSH(nb_projections=nbProjections, nb_tables=nbTabHash, w=w)
lsh.fit(allDataHisto)

lshRes = lsh.kneighbors(histoQuery, k=3)

for i in range(len(lshRes[0])):

    print("- Resultat "+str(i)+" : " +
          str(database[lshRes[1][i]])+" distance : "+str(lshRes[0][i]))
