import os
from pathlib import Path
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt 
import distance as dist

debug = True
debugPlus = False

queryPath = "./data/small/queries/152029243_b3582c36fa.jpg"
databasePath = "./data/small/images"
numpyPath = Path("./save.npy")

database = []
i = 0
for entry in os.scandir(databasePath) :

    if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file():

        database.append(str(entry.path))
        i += 1

databaseSize = i

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

def getImage (path, debug) :

    try : 

        img = cv.imread(path, cv.IMREAD_COLOR)

    except ValueError:

        print("[DEBUG] Echec du chargement de l'image")
        print("[DEBUG] Sorti du programme...")
        exit()

    if debug and img is None :

        print("[DEBUG] Echec du chargement de l'image")
        print("[DEBUG] Sorti du programme...")
        exit()

    elif debug and img.all() != None :

        print("[DEBUG] Image chargée avec succés")

    return img 

# Traitement image base de donnée -------------------------------------------------------------------------

# on verifie si un fichier de sauvegarde numpy est present


if numpyPath.is_file() :

    if debug :

        print("[DEBUG] Fichier de sauvegarde numpy trouvé") 
        print("[DEBUG] Chargement de la sauvegarde numpy...") 


    allDataHisto = np.load(str(numpyPath))


    if debug and allDataHisto is not None :

        print("[DEBUG] Sauvegarde numpy chargé avec succés")

    elif debug :

        print("[DEBUG] [ERROR] Echec du chargement de la sauvegarde numpy")

else :

    if debug :

        print("[DEBUG] [WARNING] Fichier de sauvegarde numpy non trouvé") 
        print("[DEBUG] Traitement des images de la base de donnée - Cette operation peut prendre du temps") 


    allDataHisto = np.ndarray(shape=(databaseSize , 768))
    i = 0


    for path in database :

        if debugPlus :

            print("[DEBUG] Path actuel : "+path)

        allDataHisto[i] = computeHistoVector(getImage((path), debugPlus)) 
        i += 1

    if debug :

        print("[DEBUG] Traitement terminé") 
        print("[DEBUG] Sauvegarde du resultat du traitement...") 

    np.save(str(numpyPath), allDataHisto)

    if debug and numpyPath.is_file():

        print("[DEBUG] Sauvegarde numpy terminé")

    elif debug :

        print("[DEBUG] [WARING] Echec de la sauvegarde numpy")

# Traitement image requete --------------------------------------------------------------------------------

if debug :

    print("[DEBUG] Chargement de l'image requete...")

queryImg = getImage(str(queryPath), debug)

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
    
# Recherche ---------------------------------------------------------------------------------------------

if debug :
    print("[DEBUG] Brutte force knn")

res = dist.knn_search(allDataHisto, histoQuery)

resIndex = res[0][0]
resDist = res[1][0]

print("Brute force resultat : "+str(database[resIndex])+" distance : "+str(resDist))
