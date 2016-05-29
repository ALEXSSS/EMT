from random import random
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.metrics import metrics
import numpy as np

rd = [random() for i in range(100)]
points = [[4+random(), 4 + a*3] for a in rd]
points1 = [[1+random(), 4 + a*3] for a in rd]

pointsCord = [a[0] for a in points]
pointsCord1 = [a[1] for a in points]
points1Cord = [a[0] for a in points1]
points1Cord1 = [a[1] for a in points1]
plt.plot(pointsCord, pointsCord1, 'ro')
plt.plot(points1Cord, points1Cord1, 'ro')
plt.axis([0, 6, 0, 15])
# plt.show()
for a in points: points1.append(a)
db = DBSCAN(eps=0.3, min_samples=4).fit(points1)
print(db.core_sample_indices_)
print(db.labels_)


# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)



# Black removed and is used for noise instead.
unique_labels = set(db.labels_)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
core_samples_mask=points1
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (db.labels_ == k)

    for i in range(len(db.labels_)):
        if(db.labels_[i]==k):
            plt.plot(points1[i][0], points1[i][1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=5)


plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
