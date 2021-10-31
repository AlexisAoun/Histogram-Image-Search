from sklearn.decomposition import PCA
import lsh as LSH
import os
from pathlib import Path
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import distance as dist
import timeit


def testAcp(allDataHisto, histoQuery, databasePath, queryPath):

    dimMax = 150
    dimMin = 50
    dimValues = [i for i in range(dimMin, dimMax+1)]
    precision = np.zeros_like(dimValues, dtype=np.float32)
    time = np.zeros_like(dimValues, dtype=np.float32)

    count = 0
    start = timeit.default_timer()

    resBruteKnnL2 = dist.knn_search(allDataHisto, histoQuery, k=3)
    resBruteRadiusL2 = dist.radius_search(allDataHisto, histoQuery, r=1)

    # Pour chaque dimensions allant de dimMin a dimMax
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
    plt.title('ACP radius search '+str(databasePath)+str(queryPath))
    plt.grid()
    plt.show()

    plt.plot(dimValues, time)
    plt.xlabel('Dimension')
    plt.ylabel('Time (s)')
    plt.title('ACP Radius search')
    plt.grid()
    plt.show()
