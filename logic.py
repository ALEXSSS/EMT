import sqlite3

import math
from scipy.sparse import vstack, hstack
from comtypes.safearray import numpy
from scipy.sparse import csc_matrix, csr_matrix
import time
import traceback

from scipy.spatial.distance import pdist
from sklearn.cluster import DBSCAN, KMeans, MeanShift
import scipy.sparse.sputils
import numpy as np
from sklearn.metrics import pairwise_distances

con = sqlite3.connect("firstDb.db")
cur = con.cursor()


def getListOfRgdCode():
    cursor = con.execute(
        "SELECT RgdCode from " +
        "info_rgd_desc")
    listOfRgdCode = [a[0] for a in cursor]
    return listOfRgdCode


def getListOfClicode():
    cursor = con.execute(
        "SELECT distinct CliCode from "
        "info_cli_otgr_201503")

    listOfCliCode = [a[0] for a in cursor]
    return listOfCliCode


def getSpecifyRgdCodeByClient(listOfRgdCode):
    t = time.time()
    cursor = con.execute(
        "SELECT distinct CliCode, RgdCode from "
        "info_cli_otgr_201503")
    t1 = time.time()
    print("cursor time: ", t1 - t)
    dictRgdCode = {}
    ind = 0;
    for rgd in listOfRgdCode:
        dictRgdCode[int(rgd)] = ind
        ind += 1
    dict = {}

    for a in cursor:
        try:
            if (int(a[1]) in dictRgdCode):
                if (int(a[0]) in dict):
                    dict[int(a[0])].append(dictRgdCode[int(a[1])])
                else:
                    dict[int(a[0])] = []
                    dict[int(a[0])].append(dictRgdCode[int(a[1])])
        except Exception:
            print(a[1])
            traceback.print_exc()
    t2 = time.time()
    print("list time: ", t2 - t1)
    return (dict, dictRgdCode)


def createCsrMatrixByArraysOfIndex(allcli, sizeOfRgdCode):
    newAllcli = {}
    for key in allcli.keys():
        indices = allcli[key]
        vector = [1] * len(indices)
        newAllcli[key] = csr_matrix((vector, indices, [0, len(indices)]), shape=(1, sizeOfRgdCode), dtype=float)
    return newAllcli


def KMEANScalculate(allcli, sizeOfRgdCode):
    arrStack = csr_matrix((1, sizeOfRgdCode), dtype=float).toarray()
    i = 0;
    j = 0;
    size = 10000
    for key in allcli.keys():
        i += 1
        arrStack = vstack((arrStack, allcli[key]))
        print(i)
       # if (i >= size): break
    print("kmeans is working")
    t1 = time.time()
    zx = KMeans(n_clusters=100,init='k-means++', n_init=32,max_iter=1000, precompute_distances=False,tol=0.01,n_jobs=-1).fit(arrStack)
    # zx =MeanShift().fit(arrStack)
    t2 = time.time()
    print("time for kmeans: ",t2-t1)
    print("Complete Kmeans")
    if (True):
        np.save("C:\\Users\\Alex\\PycharmProjects\\termWr\\labels", zx.labels_)
        # np.load("C:\\Users\\Alex\\PycharmProjects\\termWr\\labels.npy")
        np.save("C:\\Users\\Alex\\PycharmProjects\\termWr\\centers", zx.cluster_centers_)
        print("Complete save")

def readKmeansData():
    labels=np.load("C:\\Users\\Alex\\PycharmProjects\\termWr\\labels.npy")
    centres=np.load("C:\\Users\\Alex\\PycharmProjects\\termWr\\centers.npy")
    return (labels,centres)


def getDistanceMatrix(allcli):
    size = len(allcli.keys())
    arr = np.zeros((size, size))
    i = 0
    j = 0
    dist = 0
    dict = {}
    for key in allcli.keys():
        j = 0
        print(i)
        for key1 in allcli.keys():
            if (not (i, j) in dict):
                dist = getDistance(allcli[key], allcli[key1])
                dict[(i, j)] = dist
                dict[(j, i)] = dist
            else:
                dist = dict[(i, j)]
            arr[i][j] = dist
            arr[j][i] = dist
            j += 1
        i += 1


def getDistance(x, x1):
    cur = []
    search = []
    if (len(x) > len(x1)):
        cur = x1
        search = x
    else:
        cur = x
        search = x1
    sum = 0
    # тут можно изменить на количество не совпадений в малом векторе
    # вообщем можно её менять по-разному
    for item in cur:
        if (item in search):
            sum += 1
    return len(cur) + len(search) - 2 * sum

def mainLogicDoKmeans():
    listOfCliCode = getListOfClicode()
    listOfRgdCode = getListOfRgdCode()
    print("length CliCode: ", len(listOfCliCode))
    print("length RgdCode: ", len(listOfRgdCode))
    ret = getSpecifyRgdCodeByClient(listOfRgdCode)
    allcli = ret[0]
    newAllcli = createCsrMatrixByArraysOfIndex(allcli, len(listOfRgdCode))
    KMEANScalculate(newAllcli, len(listOfRgdCode))

def createSetsOfClients(labels):
    dict={}
    for i in range(len(labels)):
        if(labels[i] in dict):
            dict[labels[i]].append(i)
        else:
            dict[labels[i]]=[]
            dict[labels[i]].append(i)
    return dict
def generateRandomVectors(number,size):
    list=[]
    for i in range(number):
        list.append(np.random.random_sample((size,)))
    return list
#0.21514248847961426
def BindAllVectorsInBunch(centres,allcli):
    dict={}
    kol=0
    for i in allcli.keys():
        t=time.time()
        if(kol==10000): break
        #print(kol)
        kol+=1
        mi=10000000000
        fixj=0
        ark=allcli[i].todense()
        for j in range(len(centres)):
            #dist=pairwise_distances(centres[j],ark)
            dist = np.linalg.norm(centres[j]-ark)
            # k=centres[j]-ark
            # dist = math.sqrt(np.dot(k, k.T))
            # ar=np.vstack((ark,centres[j]))
            # dist=pdist(ar,'euclidean')
            if(mi>dist):
                mi=dist
                fixj=j
        if(j in dict):
            dict[j].append(i)
        else:
            dict[j]=[]
            dict[j].append(i)
        print(time.time()-t)
    return  dict

def readInterestingDataAboutKmeans():
    pair=readKmeansData()
    labels=pair[0]
    centres=pair[1]
    dict=createSetsOfClients(labels)
    print("size: ",len(dict.keys()))
    for i in dict.keys():
        print(len(dict[i]))

if __name__ == "__main__":
    listOfCliCode = getListOfClicode()
    listOfRgdCode = getListOfRgdCode()
    print("length CliCode: ", len(listOfCliCode))
    print("length RgdCode: ", len(listOfRgdCode))
    ret = getSpecifyRgdCodeByClient(listOfRgdCode)
    allcli = ret[0]
    newAllcli = createCsrMatrixByArraysOfIndex(allcli, len(listOfRgdCode))
    centres=generateRandomVectors(100,len(listOfRgdCode))
    print("Random vectors is generated!")

    dict=BindAllVectorsInBunch(centres,newAllcli)
    for i in dict.keys():
        print(i," ",len(dict[i]))
