from comtypes.safearray import numpy

rs2 = ['205010', '30100101', '30100101', '50101010', '502210']
rs1 = ['205010', '10101005', '10101005', '502210', '502210']
rs3 = []
rs3.append(rs2)
rs3.append(rs1)
print(rs2)
print(rs1)
arr = numpy.zeros((5, 5), dtype=numpy.float)
dictNodes = {'205010': 0, '30100101': 1, '10101005': 2, '50101010': 3, '502210': 4}
arrKol = numpy.zeros((5,))
ind1 = 0
setRep = set()
for rs in rs3:
    setRep = set()
    for j in range(len(rs)):
        arrKol[dictNodes[rs[j]]] += 1
        for k in range(j + 1, len(rs)):
            if (not dictNodes[rs[j]] == dictNodes[rs[k]]):
                # print(dictNodes[dict[i][j]]," ",dictNodes[dict[i][k]]," ","+1")
                if ((rs[j], rs[k]) in setRep):
                    continue
                if (dictNodes[rs[j]] == 2 and dictNodes[rs[k]] == 4):
                    print("pass: ", ind1, "j: ", j, "k: ", k)
                    print("!", ind1, "rs[j]: ", rs[j], "rs[k]: ", rs[k])
                    print()
                setRep.add((rs[j], rs[k]))
                arr[dictNodes[rs[j]]][dictNodes[rs[k]]] += 1
                arr[dictNodes[rs[k]]][dictNodes[rs[j]]] += 1
    ind1 += 1
for i in range(5):
    for j in range(5):
        arr[i][j]/=arrKol[i]
print(arrKol)
print(arr)
