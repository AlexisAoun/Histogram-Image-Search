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

def buildQueryData(debug = False):

    i = 0
    for entry in os.scandir(testQueryFolderPath):

        if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():

            testQueryDatabase.append(str(entry.path))
            i += 1

    testQuerySize = i
    testQueryData = np.ndarray(shape=(testQuerySize, 768))
    i = 0

    for path in testQueryDatabase :

        if debug :

            print("[DEBUG] "+str(path))

        testQueryData[i] = utils.computeHistoVector(utils.getImage(path, False))
        i+=1
    
    return testQueryData


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

def testLsh (data) :
    queryData = buildQueryData()

    bf = NearestNeighbors(n_neighbors=1, algorithm="brute")
    bf.fit(data)
    ground_results = bf.kneighbors(queryData, n_neighbors=1)
    ground_indices = ground_results[1]

    # Influence du facteur W

    max = 11
    w_values = [0.05 * i for i in range(1, max)]
    precisions = []
    inspected_avgs = []

    for w in w_values:

        print("Valeur de W:%f" % w)
        lsh = LSH.LSH(nb_projections=20, nb_tables=8, w=w)
        lsh.fit(data)
        match_count = 0
        inspected_count = 0

        for query in queryData:

            valeurTerrain = dist.knn_search(data, query, k=5)
            lsh_result = lsh.kneighbors(query, k=5)

            lsh_index = lsh_result[1]
            inspected_count += lsh_result[2]

            valeurTerrainIndex = valeurTerrain[0]

            for i in range(5):
                for j in range(5):
                    if lsh_index[i] == valeurTerrainIndex[j]:
                        match_count+=1
            

        precision = match_count / (len(queryData)*5)
        precisions.append(precision)
        print("precision: %f" % precision)

        inspected_avg = inspected_count / len(queryData)
        inspected_avgs.append(inspected_avg)
        print("inspected data: %f" % inspected_avg)

    # courbe de la précision en fonction de W
    plt.plot(w_values, precisions, label="W", color="blue")
    plt.legend()
    plt.show()

    # courbe du nombre de données inspectés en moyenne en fonction de W
    plt.plot(w_values, inspected_avgs, label="W", color="blue")
    plt.legend()
    plt.show()
'''
    # Influence du nombre de table de hachage
    precisions = []
    ratio_avgs = []
    data_size = len(data)
    for nt in range(1,7):
        print("Nombre de tables:%d" % nt)
        lsh = LSH.LSH(nb_projections=10, nb_tables=nt, w=1.0)
        lsh.fit(data)
        match_count = 0
        inspected_count = 0
        ratio_sum = 0
        for i, query in enumerate(queryData):
            lsh_result = lsh.kneighbors(query, k=1)
            lsh_index = lsh_result[1][0]
            match_count += 1 if lsh_index == ground_indices[i] else 0
            inspected_count += lsh_result[2]
            ratio = inspected_count / data_size
            ratio_sum += ratio

        precision = match_count / len(queryData) #same question
        precisions.append(precision)
        print("precision: %f" % precision)

        ratio_avg = ratio_sum / len(queryData)
        ratio_avgs.append(ratio_avg)
        print("average ratio : %f" % ratio_avg)

    # Comportement en fonction de la la dimension de la donnée
    max_dim = data.shape[1]
    for dim in range(10, max_dim, 20):
        print("Dimension:%d" % dim)
        red_ds_glove = data[:, :dim]
        red_pr_glove = queryData[:, :dim]
        bf = NearestNeighbors(n_neighbors=1, algorithm='brute')
        bf.fit(red_ds_glove)
        ground_results = bf.kneighbors(red_pr_glove, n_neighbors=1)
        ground_indices = ground_results[1]
        for nproj in [5, 8, 10]:
            print("Nombre de projection:%d" % nproj)
            lsh = LSH(nb_projections=nproj, nb_tables=2, w=1.0)
            lsh.fit(red_ds_glove)
            match_count = 0
            for i, query in enumerate(red_pr_glove):
                lsh_result = lsh.kneighbors(query, k=1)
                lsh_index = lsh_result[1][0]
                match_count += 1 if lsh_index == ground_indices[i] else 0

            precision = match_count / len(red_pr_glove)
            print("precision: %f" % precision)

'''