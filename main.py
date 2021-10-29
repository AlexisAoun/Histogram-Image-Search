from sklearn.decomposition import PCA
import lsh as LSH
import os
from pathlib import Path
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import distance as dist
import timeit


debug = False
debugPlus = False

queryPath = "./data/small/queries/2090339522_d30d2436f9.jpg"
databasePath = "./data/big/images"
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
        print("[DEBUG] Sortie du programme...")
        exit()

    if debug and img is None:

        print("[DEBUG] Echec du chargement de l'image")
        print("[DEBUG] Sortie du programme...")
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

        allDataHisto[i] = computeHistoVector(getImage((path), debugPlus))
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

queryImg = getImage(str(queryPath), debug)

if debug:

    print("[DEBUG] Calcul du vecteur carateristique de la requete...")

histoQuery = computeHistoVector(queryImg)

if debug:

    if histoQuery is not None and histoQuery.shape == (768,):

        print("[DEBUG] Vecteur carateristique de la requete calcule (shape OK)")

    else:

        print("[DEBUG] Echec du calcul du vecteur caracteristique de la requete")
        print("[DEBUG] Sortie du programme...")
        exit()

# Recherche ---------------------------------------------------------------------------------------------

# Brute force : meilleurs resultats possibles
if debug:
    print("[DEBUG] Calcul Brute knn et radius L2")

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


# ACP, mesure de la précision et du temps d'execution
dimMax = 150
dimMin = 140
dimValues = [i for i in range(dimMin, dimMax+1)]
precision = np.zeros_like(dimValues, dtype=np.float32)
time = np.zeros_like(dimValues, dtype=np.float32)

count = 0
start = timeit.default_timer()
for dimensionArivee in range(dimMin, dimMax+1):

    pca = PCA(n_components=dimensionArivee)
    dataPCA = pca.fit_transform(allDataHisto)

    histoQueryPCA = histoQuery - pca.mean_
    VecteurP = pca.components_
    histoQueryPCA = histoQueryPCA@VecteurP.T

    resBruteKnnACP = dist.knn_search(dataPCA, histoQueryPCA, k=3)
    resBruteRadiusACP = dist.radius_search(dataPCA, histoQueryPCA, r=1)

    # Pour tous les résultats retournés par la recherche en ACP
    match = 0
    for i in range(len(resBruteRadiusACP[0])):

        # On vérifie s'ils correspondent dans la liste des réponses justes
        for j in range(len(resBruteRadiusL2[0])):
            if resBruteRadiusACP[0][i] == resBruteRadiusL2[0][j]:
                match += 1

    precision[count] = match/len(resBruteRadiusACP[0])
    stop = timeit.default_timer()
    time[count] = stop-start
    count += 1

plt.plot(dimValues, precision)
plt.xlabel('Dimension')
plt.ylabel('Precision')
plt.title('ACP radius search')
plt.grid()
plt.show()

plt.plot(dimValues, time)
plt.xlabel('Dimension')
plt.ylabel('Time (ms)')
plt.title('ACP Radius search')
plt.grid()
plt.show()


# PCA unique
dimensionArivee = 480
pca = PCA(n_components=dimensionArivee)
dataPCA = pca.fit_transform(allDataHisto)

histoQueryPCA = histoQuery - pca.mean_
VecteurP = pca.components_
histoQueryPCA = histoQueryPCA@VecteurP.T

resBruteKnnACP = dist.knn_search(dataPCA, histoQueryPCA, k=3)
resBruteRadiusACP = dist.radius_search(dataPCA, histoQueryPCA, r=1)
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
