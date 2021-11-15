from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np
import timeit
import os

import lsh as LSH
import distance as dist
import utils as utils

testQueryFolderPath = "./data/big/queries"
testQueryDatabase = []
testQuerySize = 0


# fonction construisant le tableau de vecteurs des images dans le dossier query specifier dans testQueryFolderPath
def buildQueryData(debug=False):

    i = 0
    for entry in os.scandir(testQueryFolderPath):

        if (
            entry.path.endswith(".jpg") or entry.path.endswith(".png")
        ) and entry.is_file():

            testQueryDatabase.append(str(entry.path))
            i += 1

    testQuerySize = i
    testQueryData = np.ndarray(shape=(testQuerySize, 768))
    i = 0

    for path in testQueryDatabase:

        if debug:

            print("[DEBUG] " + str(path))

        testQueryData[i] = utils.computeHistoVector(utils.getImage(path, False))
        i += 1

    return testQueryData


# fonction de test acp
def testAcp(allDataHisto, histoQuery, databasePath, queryPath):

    dimMax = 150
    dimMin = 50
    dimValues = [i for i in range(dimMin, dimMax + 1)]
    precision = np.zeros_like(dimValues, dtype=np.float32)
    time = np.zeros_like(dimValues, dtype=np.float32)

    count = 0
    start = timeit.default_timer()

    resBruteKnnL2 = dist.knn_search(allDataHisto, histoQuery, k=3)
    resBruteRadiusL2 = dist.radius_search(allDataHisto, histoQuery, r=1)

    # Pour chaque dimensions allant de dimMin a dimMax
    for dimensionArivee in range(dimMin, dimMax + 1):

        pca = PCA(n_components=dimensionArivee)
        dataPCA = pca.fit_transform(allDataHisto)

        histoQueryPCA = histoQuery - pca.mean_
        VecteurP = pca.components_
        histoQueryPCA = histoQueryPCA @ VecteurP.T

        resBruteKnnACP = dist.knn_search(dataPCA, histoQueryPCA, k=3)
        resBruteRadiusACP = dist.radius_search(dataPCA, histoQueryPCA, r=1)

        # Pour tous les résultats retournés par la recherche en ACP
        match = 0
        for i in range(len(resBruteRadiusACP[0])):

            # On vérifie s'ils correspondent dans la liste des réponses justes
            for j in range(len(resBruteRadiusL2[0])):
                if resBruteRadiusACP[0][i] == resBruteRadiusL2[0][j]:
                    match += 1

        precision[count] = match / len(resBruteRadiusACP[0])
        stop = timeit.default_timer()
        time[count] = stop - start
        count += 1

    plt.plot(dimValues, precision)
    plt.xlabel("Dimension")
    plt.ylabel("Precision")
    plt.title("ACP radius search " + str(databasePath) + str(queryPath))
    plt.grid()
    plt.show()

    plt.plot(dimValues, time)
    plt.xlabel("Dimension")
    plt.ylabel("Time (s)")
    plt.title("ACP Radius search")
    plt.grid()
    plt.show()


# fonction testant un tableau de vecteur query avec les param LSH specifier
# retourne la precision et le ration de vecteur inspecte
def testLsh(data, queryData, w, nbTab, nbProj, k):
    precisions = []
    insptected_avg = []

    lsh = LSH.LSH(nb_projections=nbProj, nb_tables=nbTab, w=w)
    lsh.fit(data)

    match_count = 0
    inspected_count = 0
    ratioSum = 0
    ratioAvg = 0

    for query in queryData:

        valeurTerrain = dist.knn_search(data, query, k=k)
        valeurTerrainIndex = valeurTerrain[0]

        lshResult = lsh.kneighbors(query, k=k)
        lshIndex = lshResult[1]

        inspected_count += lshResult[2]
        ratioSum += inspected_count / len(data)

        for i in range(len(lshIndex)):
            for j in range(len(valeurTerrainIndex)):
                if lshIndex[i] == valeurTerrainIndex[j]:
                    match_count += 1

    precision = match_count / (len(queryData) * k)
    ratioAvg = ratioSum / len(queryData)

    return precision, ratioAvg


# fonction testant l ensemble des param lsh
# imprime les valeurs de la precision et du ratio, et trace les courbes correspondantes
def testCompletLsh(data):
    queryData = buildQueryData()
    print("Test de l'influence de W")
    # Influence du facteur W -------------------------------------------------------------------------------------
    max = 20
    w_values = [0.025 * i for i in range(0, max)]
    w_values[0] = 0.001
    precisions = []
    ratioAvgs = []

    for w in w_values:

        print("Valeur de W:%f" % w)
        res = testLsh(data, queryData, w, 5, 8, 5)

        precisions.append(res[0])
        print("precision: %f" % res[0])

        ratioAvgs.append(res[1])
        print("ratio data: %f" % res[1])

    # courbe de la précision en fonction de W
    plt.plot(w_values, precisions, label="Infleunce W sur precision", color="blue")
    plt.legend()
    plt.show()

    # courbe du nombre de données inspectés en moyenne en fonction de W
    plt.plot(
        w_values,
        ratioAvgs,
        label="Influence W sur nbre d'elements inspectes",
        color="blue",
    )
    plt.legend()
    plt.show()

    # Influence du nombre de table de hachage -------------------------------------------------------------------
    print("Test de l'influence du nombre de table de hachage")
    precisions = []
    ratioAvgs = []
    for nt in range(1, 11):
        print("Nombre de tables:%d" % nt)
        res = testLsh(data, queryData, 0.065, nt, 8, 5)

        precisions.append(res[0])
        print("precision: %f" % res[0])

        ratioAvgs.append(res[1])
        print("ratio data : %f" % res[1])

    plt.plot(
        range(1, 11), precisions, label="Influence nb tab sur precision", color="blue"
    )
    plt.legend()
    plt.show()

    plt.plot(
        range(1, 11),
        ratioAvgs,
        label="Influence nb tab sur inspected avgs",
        color="blue",
    )
    plt.legend()
    plt.show()

    # Comportement en fonction du nbre de projection ------------------------------------------------------------
    print("Test de l'influence du nombre de projection")
    ratioAvgs = []
    precisions = []
    for nproj in range(1, 20):
        print("Nombre de projection:%d" % nproj)

        res = testLsh(data, queryData, 0.065, 3, nproj, 5)

        precisions.append(res[0])
        print("precision: %f" % res[0])

        ratioAvgs.append(res[1])
        print("Ratio data : %f" % res[1])

    plt.plot(
        range(1, 20), precisions, label="Influence nb proj sur precision", color="blue"
    )
    plt.legend()
    plt.show()

    plt.plot(
        range(1, 20),
        ratioAvgs,
        label="Influence nb proj sur inspected avgs",
        color="blue",
    )
    plt.legend()
    plt.show()
