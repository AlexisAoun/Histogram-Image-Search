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

# Brute force : meilleurs resultats possibles
'''
if debug:
    print("[DEBUG] Calcul Brute knn et radius L2")

resBruteKnnL2 = dist.knn_search(allDataHisto, histoQuery, k=3)
resBruteRadiusL2 = dist.radius_search(allDataHisto, histoQuery, r=0.7)

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

# LSH
w = 1
nbProjections = 12
nbTabHash = 1

print("")
print("Recherche LSH : W = "+str(w)+" nb projections : "+str(nbProjections))

lsh = LSH.LSH(nb_projections=nbProjections, nb_tables=nbTabHash, w=w)
lsh.fit(allDataHisto)

lshRes = lsh.kneighbors(histoQuery, k=3)

for i in range(len(lshRes[0])):

    print("- Resultat "+str(i)+" : " +
          str(database[lshRes[1][i]])+" distance : "+str(lshRes[0][i]))


'''

# ACP, mesure de la précision et du temps d'execution ------------------------------------------------

# PCA unique --------------------------------------------------------------------------
'''
dimensionArivee = 100
pca = PCA(n_components=dimensionArivee)
dataPCA = pca.fit_transform(allDataHisto)

histoQueryPCA = histoQuery - pca.mean_
VecteurP = pca.components_
histoQueryPCA = histoQueryPCA@VecteurP.T

resBruteKnnACP = dist.knn_search(dataPCA, histoQueryPCA, k=3)
resBruteRadiusACP = dist.radius_search(dataPCA, histoQueryPCA, r=0.7)
print()
print("Image requete : "+str(queryPath))

print("Recherche knn ACP n dimensions : "+str(dimensionArivee))
for i in range(len(resBruteKnnACP[0])):

    print("- Resultat "+str(i)+" : " +
          str(database[resBruteKnnACP[0][i]])+" distance : "+str(resBruteKnnACP[1][i]))


print("")
print("Recherche radius L2 ACP")
for i in range(len(resBruteRadiusACP[0])):

    print("- Resultat "+str(i)+" : " +
          str(database[resBruteRadiusACP[0][i]])+" distance : "+str(resBruteRadiusACP[1][i]))

'''
#print("[DEBUG] Test acp en cours...")
#tests.testAcp(allDataHisto, histoQuery, databasePath, queryPath)

print("[DEBUG] Test lsh en cours...")
tests.testLsh(allDataHisto)