from sklearn.decomposition import PCA
import lsh as LSH
import os
from pathlib import Path
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import distance as dist
import timeit
import tests as tests
import utils as utils


debug = True
debugPlus = False

queryPath = "./data/small/queries/3613323772_d15cef66d1.jpg"
databasePath = "./data/big/images"
numpyPath = Path("./savebig.npy")

database = []
i = 0
for entry in os.scandir(databasePath):

    if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():

        database.append(str(entry.path))
        i += 1

databaseSize = i

# Traitement image base de donnée -------------------------------------------------------------------------

# on verifie si un fichier de sauvegarde numpy est present


if numpyPath.is_file():

    if debug:

        print("[DEBUG] Fichier de sauvegarde numpy detecte")
        print("[DEBUG] Chargement de la sauvegarde numpy...")

    allDataHisto = np.load(str(numpyPath))

    if debug and allDataHisto is not None:

        print("[DEBUG] Sauvegarde numpy chargee avec succes")

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

        allDataHisto[i] = utils.computeHistoVector(utils.getImage((path), debugPlus))
        i += 1

    if debug:

        print("[DEBUG] Traitement termine")
        print("[DEBUG] Sauvegarde du resultat du traitement...")

    np.save(str(numpyPath), allDataHisto)

    if debug and numpyPath.is_file():

        print("[DEBUG] Sauvegarde numpy terminee")

    elif debug:

        print("[DEBUG] [WARNING] Echec de la sauvegarde numpy")

# Traitement image requete --------------------------------------------------------------------------------

if debug:

    print("[DEBUG] Chargement de l'image requete...")

queryImg = utils.getImage(str(queryPath), debug)

if debug:

    print("[DEBUG] Calcul du vecteur carateristique de la requete...")

histoQuery = utils.computeHistoVector(queryImg)

if debug:

    if histoQuery is not None and histoQuery.shape == (768,):

        print("[DEBUG] Vecteur carateristique de la requete calcule (shape OK)")

    else:

        print("[DEBUG] Echec du calcul du vecteur caracteristique de la requete")
        print("[DEBUG] Sortie du programme...")
        exit()

# Recherche ---------------------------------------------------------------------------------------------

#w = 0.065
#nbTab = 3
#nbProj = 6
#
#print("test lsh w = %f , nb tab = %f , nb proj = %f" %(w, nbTab,nbProj ))
#res = tests.testLsh(allDataHisto,tests.buildQueryData(), w, nbTab, nbProj, 5)
#print(res)

tests.testCompletLsh(allDataHisto)