import math
from scipy.sparse import csc_matrix, csr_matrix
from scipy.spatial.distance import pdist
from sklearn.cluster import DBSCAN
import numpy as np
from scipy.sparse import vstack, hstack
from statsmodels.compat import scipy
from sklearn.metrics import pairwise_distances
from sklearn.cluster import DBSCAN, KMeans

# ret=(1,2)
# nme=ret[0]
# print(nme)
# dict={'b':1, 'c':2}
# print('b' in dict)
# print(2 in dict)
array = np.zeros((10,))
array[1]=1
array[4]=1
array[5]=1
array[6]=1
array[9]=1


print(array)
print()
i = 0

b = csr_matrix(array)
print(b)
array[7]=1
array[2]=1.5
print("/////////////////////////")

print(b.todense())
print(array)
# k=array-b.todense()
# dist = math.sqrt(np.dot(k, k.T))
#dist = np.linalg.norm(array-b.todense())
ar=np.vstack((array,b.todense()))
print(ar)
dist=pdist(ar,'euclidean')
print(dist)
# print()
# print(b.indptr)
# print()
# print(b.indices)
# print()
# print(b.data)

# print()
# k=[0, 3]
# k40=[0, 4]
# k1=[1, 2, 3]
# k41=[1, 2, 3,5]
# k2=[1,1,1]
# k42=[1,1,1,1]
# j=csr_matrix( (k2,k1,k), shape=(1,10))
# j1=csr_matrix( (k42,k41,k40), shape=(1,10),copy=True)
# print(j.todense())
# print(b.todense())
# g=[]
# g.append(j)
# g.append(b)

# arf=vstack((j,b))
# arf=vstack((arf,j1))
# print()
# print(arf)
# print(arf.indices)
# print(arf.indptr)
# print(j)
# print(b)
# print("!!!!!!!!!!!!!!!!!!!!!!!!!")
# print(j.todense())
# print(b.todense())
# print(j1.todense())
# print(pairwise_distances(j,b))
# print(pairwise_distances(j,j1))
# print(pairwise_distances(b,j1))
# # print(arf)
# # zx=DBSCAN(eps=2.22, min_samples=2).fit(arf)
# #zx= KMeans(n_clusters=2, init='k-means++', n_init=10, precompute_distances=False).fit(arf)
# print("///////////////////////")


