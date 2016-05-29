import sqlite3
import networkx

from comtypes.safearray import numpy
import time
import traceback
import matplotlib.pyplot as plt

con = sqlite3.connect("firstDb.db")
cur = con.cursor()


def getSpecifyClassByClient():
    t = time.time()
    cursorClasses = con.execute(
        "SELECT distinct RgdCode,ClassCode81 from " +
        "info_rgd_desc")
    dictClasses = {}
    for a in cursorClasses:
        dictClasses[a[0]] = a[1]

    cursor = con.execute(
        "SELECT distinct CliCode, RgdCode from "
        "info_cli_otgr_201503")
    t1 = time.time()
    print("cursor time: ", t1 - t)
    dict = {}
    ind = 0
    ind1 = 0
    for a in cursor:
        try:
            if (True):
                c = int(a[0])
                if (c in dict):
                    dict[int(a[0])].append(dictClasses[a[1]])
                else:
                    dict[int(a[0])] = []
                    dict[int(a[0])].append(dictClasses[a[1]])
            ind1 += 1
        except Exception:
            # print("this key doesn't exist: ",a[1])
            ind += 1
            # traceback.print_exc()
    t2 = time.time()
    print("list time: ", t2 - t1)
    print("Number of errors is: ", ind)
    print("Number of operations is: ", ind1)
    return (dict, dictClasses)


def createDictOfClasse():
    dict = {}
    cursorClasses = con.execute(
        "SELECT distinct ClassCode81 from " +
        "info_class81")
    index = 0
    for a in cursorClasses:
        dict[a[0]] = index
        index += 1
    return dict


def createGraph():
    res = getSpecifyClassByClient()
    dict = res[0]
    dictClasses = res[1]
    dictNodes = createDictOfClasse()
    arr = numpy.zeros((len(dictNodes.keys()), len(dictNodes.keys())), dtype=numpy.float)
    print("//////////////////////////////////////")
    arrKol = numpy.zeros((len(dict.keys()),))
    if (True):
        for i in dict.keys():
            setRep = set()
            for j in range(len(dict[i])):
                arrKol[dictNodes[dict[i][j]]] += 1
                for k in range(j + 1, len(dict[i])):
                    if ((dictNodes[dict[i][k]], dictNodes[dict[i][j]]) in setRep):
                        continue
                    if (not dictNodes[dict[i][j]] == dictNodes[dict[i][k]]):
                        # print(dictNodes[dict[i][j]]," ",dictNodes[dict[i][k]]," ","+1")
                        arr[dictNodes[dict[i][j]]][dictNodes[dict[i][k]]] += 1
                        arr[dictNodes[dict[i][k]]][dictNodes[dict[i][j]]] += 1
                        setRep.add((dictNodes[dict[i][j]], dictNodes[dict[i][k]]))
                        setRep.add((dictNodes[dict[i][k]], dictNodes[dict[i][j]]))
    numpy.save("C:\\Users\\Alex\\PycharmProjects\\termWr\\graph", arr)
    numpy.save("C:\\Users\\Alex\\PycharmProjects\\termWr\\kol", arrKol)
    # rs2 = ['205010', '30100101', '30100101', '50101010', '502210']
    # rs1 = ['205010', '10101005', '10101005','502210','502210']
    # rs3 = []
    # rs3.append(rs2)
    # rs3.append(rs1)
    # print(rs2)
    # print(rs1)
    # arr = numpy.zeros((5, 5), dtype=numpy.float)
    # dictNodes = {'205010': 0, '30100101': 1, '10101005': 2, '50101010': 3, '502210': 4}
    # arrKol = numpy.zeros((5,))
    # ind1=0
    # setRep=set()
    # for rs in rs3:
    #     setRep=set()
    #     for j in range(len(rs)):
    #         arrKol[dictNodes[rs[j]]] += 1
    #         for k in range(j + 1, len(rs)):
    #             if (not dictNodes[rs[j]] == dictNodes[rs[k]]):
    #                 # print(dictNodes[dict[i][j]]," ",dictNodes[dict[i][k]]," ","+1")
    #                 if((rs[j],rs[k]) in setRep):
    #                     continue
    #                 if(dictNodes[rs[j]]==2 and dictNodes[rs[k]]==4):
    #                     print("pass: ",ind1,"j: ",j,"k: ",k)
    #                     print("!",ind1,"rs[j]: ",rs[j],"rs[k]: ",rs[k])
    #                     print()
    #                 setRep.add((rs[j],rs[k]))
    #                 arr[dictNodes[rs[j]]][dictNodes[rs[k]]] += 1
    #                 arr[dictNodes[rs[k]]][dictNodes[rs[j]]] += 1
    #     ind1+=1





if __name__ == "__main__":
    #createGraph()
    d = numpy.load("C:\\Users\\Alex\\PycharmProjects\\termWr\\graph.npy")
    dkol = numpy.load("C:\\Users\\Alex\\PycharmProjects\\termWr\\kol.npy")
    print(d)
    for i in range(1324):
        for j in range(1324):
            if(not dkol[i]==0):
                d[i][j]=d[i][j]/(dkol[i])
                if(d[i][j]>1):
                        print("! ",d[i][j]," ",dkol[i], dkol[j])

    for i in range(1324):
        for j in range(1324):
            if(d[i][j]<0.52): d[i][j]=0
    # numpy.save("C:\\Users\\Alex\\PycharmProjects\\termWr\\newgr", d)
    #
    # d = numpy.load("C:\\Users\\Alex\\PycharmProjects\\termWr\\newgr.npy")
    G = networkx.DiGraph()
    #G = networkx.Graph()
    for i in range(1324):
        for j in range(1324):
            if (d[i][j] > 0):
                G.add_edge(i, j)
                print(i, " ", j)

    print("Run!")
    cursorNames = con.execute(
        "SELECT distinct ClassCode81,ClassName81 from " +
        "info_class81")
    dictNames={}
    dictRevClasses={}
    for a in cursorNames:
        dictNames[a[0]]=[a[1]]
    dc=createDictOfClasse()
    for a in dc:
        dictRevClasses[dc[a]]=dictNames[a]
    # G1 = networkx.DiGraph()
    # G1.add_edge(1,2)
    # G1.add_edge(2,3)
    # G1.add_edge(3,1)
    # G1.add_edge(3,10)
    # G1.add_edge(10,1)
    # print(len(G.edges()))
    A = networkx.simple_cycles(G)
    #A = networkx.find_cliques(G)
    # print(list(networkx.find_cliques(G)))
    # networkx.draw(G,pos=networkx.spring_layout(G))
    # plt.show()
    als=list(A)
    for ls in als:
        print("[",end="")
        for node in ls:
            print(dictRevClasses[node],end=" ")
        print("]",end="")
        print()

