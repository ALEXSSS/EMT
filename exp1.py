from scipy.sparse import csc_matrix, csr_matrix
from sklearn.cluster import DBSCAN, KMeans, MeanShift
import numpy as np
from scipy.sparse import vstack, hstack
from statsmodels.compat import scipy
from sklearn.metrics import pairwise_distances, euclidean_distances
print(np.zeros(5,))
a={"1fdgfd":'a',"2":'b'}
#a=[1,0,2,3,4,1000]
print("1fdgfd" in a.keys())
arr=[[0,1,0,1],[1,1,1,0],[0,0,0,1],[0,0,0,1],[1,1,1,1],[1,1,2,1]]
narr=np.array(arr)

#np.save("C:\\Users\\Alex\\PycharmProjects\\termWr\\1",arr)
# d=np.load("C:\\Users\\Alex\\PycharmProjects\\termWr\\1.npy")
# print(d)
print(np.amin(narr,axis=0))
print(np.amin(narr,axis=0))
print(narr)
print(np.max(euclidean_distances(narr, narr),axis=0))
print((euclidean_distances(narr, narr)))
print("//////////////////////////////////////")
z=MeanShift().fit(arr)
print("//////////////////////////////////////")
print(z)
