import csv, sqlite3
import os
import random

import numpy as np
import matplotlib.pyplot as plt
from numpy import array
from scipy.cluster.vq import vq, kmeans, whiten, kmeans2

con = sqlite3.connect("firstDb.db")
cur = con.cursor()


def createcolumns(dr):
    s = "";
    j = len(dr.fieldnames)
    k = 0;
    for i in dr.fieldnames:
        k += 1
        if (k == 1):
            s += "( " + i
        else:
            if (k != j):
                s += " , " + i
            else:
                s += " , " + i + " )"
    return s


def createemptycolumns(dr):
    s = "";
    j = len(dr.fieldnames)
    k = 0;
    for i in dr.fieldnames:
        k += 1
        if (k == 1):
            s += "( " + "?"
        else:
            if (k != j):
                s += " , " + "?"
            else:
                s += " , " + "?" + " )"
    return s


def build_table(path, s):
    with open(path + "\\" + s + ".csv", 'r') as fin:  # `with` statement available in 2.5+
        dr = csv.DictReader(fin, delimiter=';')  # comma is default delimiter
        column = createcolumns(dr)
        cur.execute("CREATE TABLE " + s + " " + column)
        to_db = []
        temp = []
        for i in dr:
            temp = []
            for j in dr.fieldnames:
                temp.append(i[j])
            to_db.append(temp)
        emptyColumn = createemptycolumns(dr)
        cur.executemany("INSERT INTO " + s + " " + column + " VALUES " + emptyColumn + ";", to_db)
        con.commit()


def rambler(path):
    ls = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            ls.append(file)
    return ls


def deleteAll(listoffiles):
    for namefull in listoffiles:
        name, sep, format = namefull.partition('.')
        con.execute("Delete from " + name)
        con.execute("drop table if exists " + name)
        print("delete: "+name)


def buildallbase():
    path = "C:\\Users\\Alex\\Desktop\\courseWorkFromCloud\\DataMining"
    listoffiles = rambler(path)
    try:
        deleteAll(listoffiles)
    except Exception:
        print("delete is completed")
    for namefull in listoffiles:
        name, sep, format = namefull.partition('.')
        build_table(path, name)
    print("base has been built")


if __name__ == "__main__":
    buildallbase()
    # cursor = con.execute("SELECT a.CliCode from info_cli_otgr_201503"+
    #                      " as a,info_cli_otgr_201501 as b "+
    #                      "where CAST(a.CliCode AS INTEGER)=CAST(b.CliCode AS INTEGER)")
    # cursor = con.execute(
    #     "SELECT CliCode, RgdGroupCode, sum(RgdQuant) from info_cli_otgr_201503 as a where RgdGroupCode=\"11\" group by CliCode, RgdGroupCode ")
    # i = 0;
    # array = [a[2] for a in cursor]
    #
    # whitened = whiten(array)
    # # print(whitened)
    # a = kmeans(whitened, 8)
    # print(a[0])
    # arrayrd = [7 + (random.random() - 0.5) * 6 for b in whitened]
    # result = vq(whitened, a[0])
    # colors=['ob','or','sg']
    # for i in range(len(whitened)):
    #     plt.plot(whitened[i], arrayrd[i], colors[i%3])
    # plt.axis([0, 50, 0, 50])
    # plt.show()
