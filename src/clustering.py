from explore_data import buyer_history
from make_trace_bis import trace
from find_dir import cmd_folder

import pandas as pd
from leven import levenshtein
import numpy as np
from sklearn.cluster import DBSCAN
import sklearn.cluster
import distance
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import AgglomerativeClustering

replacement = pd.DataFrame(columns=['event','lettre'])
i= 0
xd = 'abcdefghijklmnopqrstuvwxyz'
for word in buyer_history.event.unique():
    replacement.loc[len(replacement)] = [word,xd[i]]
    i+=1
tt = pd.DataFrame(columns=['uid','event'])
for i in range(len(trace)):
    uid = trace[i]['id']
    event = ""
    for j in range(len(trace[i]['trace'])):
        lere = trace[i]['trace'][j]['event']
        lettre = ''.join(replacement['lettre'][replacement['event']==lettre])
        event += lettre
    tt.loc[len(tt)] = [uid,event]

######### LEVENSHTEIN avec complexité optimale mais ASSYMETRIQUE
# def llevenshtein(source, target):
#     if len(source) < len(target):
#         return llevenshtein(target, source)
#
#     # So now we have len(source) >= len(target).
#     if len(target) == 0:
#         return len(source)
#
#     # We call tuple() to force strings to be used as sequences
#     # ('c', 'a', 't', 's') - numpy uses them as values by default.
#     source = np.array(tuple(source))
#     target = np.array(tuple(target))
#
#     # We use a dynamic programming algorithm, but with the
#     # added optimization that we only need the last two rows
#     # of the matrix.
#     previous_row = np.arange(target.size + 1)
#     for s in source:
#         # Insertion (target grows longer than source):
#         current_row = previous_row + 1
#
#         # Substitution or matching:
#         # Target and source items are aligned, and either
#         # are different (cost of 1), or are the same (cost of 0).
#         current_row[1:] = np.minimum(
#                 current_row[1:],
#                 np.add(previous_row[:-1], target != s))
#
#         # Deletion (target grows shorter than source):
#         current_row[1:] = np.minimum(
#                 current_row[1:],
#                 current_row[0:-1] + 1)
#
#         previous_row = current_row
#
#     return previous_row[-1]

######### CALCUL DISTANCE MATRIX

data = tt['event']
n = len(data)
data = data.ix[0:n]

# maat = pd.read_csv(cmd_folder+ 'output/data/maat.csv',header= None)

maat = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        maat[i][j] = levenshtein(data[i],data[j])
# for i in range(n):
#     for j in range(n):
#         mat0[i][j] = levenshtein(data0.iloc[i]['event'],data0.iloc[j]['event'])
#
# mat0
maat = np.array(maat)

# i, j = np.ogrid[:n,:n]
# y = llevenshtein(data[i],data[j])

######### DBSCAN

db = DBSCAN(metric='precomputed', eps=0.1, min_samples=10).fit(maat)

labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_clusters_
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True

xdd = pd.DataFrame(labels)
pd.DataFrame([xdd[0]==-1]).sum(axis =1)
pd.DataFrame([xdd[0]==-1]).shape

def plot_hist(clusters,name):
    plt.figure(figsize=(12, 9))

    # Remove the plot frame lines. They are unnecessary chartjunk.
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()


    # Along the same vein, make sure your axis labels are large
    # enough to be easily read as well. Make them slightly larger
    # than your axis tick labels so they stand out.
    plt.xlabel("Nombre de clusters", fontsize=12)
    plt.ylabel("Nombre d'individus par cluster", fontsize=12)
    plt.hist(clusters,color="#3F5D7D", bins=30)

    plt.savefig(cmd_folder+"output/picture/"+name+"hist.png", bbox_inches='tight')
    plt.show()

plot_hist(xdd,"hist")

######### KMEANS

num_clusters = 15

km = KMeans(n_clusters=num_clusters)

%time km.fit(maat)
clusters = km.labels_.tolist()
clusters
km.cluster_centers_.shape
inertie = km.inertia_

plot_hist(clusters,"histKM")

# for i in range(15):
#     print(donnees[donnees['cluster'] == i].trace.str.len().mean())

donnees = pd.DataFrame(columns = ['trace','cluster'])
donnees['trace'] = data
donnees['cluster'] = clusters
index = donnees[donnees['cluster'] == 0].index
cluster0 = data.loc[index]

######### AgglomerativeClustering

ac = sklearn.cluster.AgglomerativeClustering(n_clusters = 15,affinity = "precomputed",linkage = "average").fit(maat)
ac.labels_

plot_hist(ac.labels_,"histAC")

lab = pd.DataFrame(ac.labels_)
lab[lab[0] == 6].shape

######### MULTIDIMENSIONAL SCALING

mds = sklearn.manifold.MDS(n_components=2, max_iter=3000, eps=1e-9,
                   dissimilarity="precomputed", n_jobs=1)
pos = mds.fit(maat).embedding_

pos = sklearn.manifold.MDS(n_components = 2,dissimilarity = 'precomputed').fit(maat.astype(np.float64)).embedding_

pos3D = sklearn.manifold.MDS(n_components = 3,dissimilarity = 'precomputed').fit(maat.astype(np.float64)).embedding_

def plot_mds(pos,clusters,j,name):
    colors = ['black','green','red','cyan','magenta','yellow','blue','white','crimson','pink','navy','coral','maroon','y','lime','azure','green']
    i = 0
    if j == 2:
        plt.figure(figsize=(12, 9))

    # Remove the plot frame lines. They are unnecessary chartjunk.
        ax = plt.subplot(111)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # Ensure that the axis ticks only show up on the bottom and left of the plot.
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()


    # Along the same vein, make sure your axis labels are large
    # enough to be easily read as well. Make them slightly larger
    # than your axis tick labels so they stand out.
        plt.xlabel("Dimension 1", fontsize=12)
        plt.ylabel("Dimension 2", fontsize=12)
        for x,y in zip(pos[:,0],pos[:,1]):
            plt.scatter(x,y, color=colors[clusters[i]], lw=0, label='MDS')
            i+=1
        plt.savefig(cmd_folder+"output/picture/"+name+".png", bbox_inches='tight')
        plt.show()
    else:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('Dimension 1')
        ax.set_ylabel('Dimension 2')
        ax.set_zlabel('Dimension 3')
        for x,y,z in zip(pos[:,0],pos[:,1],pos[:,2]):
            ax.scatter(x,y,z,color=colors[clusters[i]], lw=0, label='MDS')
            i+=1
        plt.savefig(cmd_folder+"output/picture/"+name+".png", bbox_inches='tight')
        plt.show()

plot_mds(pos,clusters,2,"kmeans2D")
plot_mds(pos3D,clusters,3,"kmeans3D")
plot_mds(pos3D,labels,3,"DBSCAN3D")
plot_mds(pos,labels,2,"DBSCAN2D")

plot_mds(pos,ac.labels_,2,"CAH2D")

plot_mds(pos3D,ac.labels_,3,"CAH3D")

######### SWAG MAIS AUCUN RAPPORT

import time
import matplotlib.pyplot as plt
import numpy as np

from sklearn.neighbors import kneighbors_graph

# Generate sample data
n_samples = 1500
np.random.seed(0)
t = 1.5 * np.pi * (1 + 3 * np.random.rand(1, n_samples))
x = t * np.cos(t)
y = t * np.sin(t)


X = np.concatenate((x, y))
X += .7 * np.random.randn(2, n_samples)
X = X.T
X.shape
data.shape
# Create a graph capturing local connectivity. Larger number of neighbors
# will give more homogeneous clusters to the cost of computation
# time. A very large number of neighbors gives more evenly distributed
# cluster sizes, but may not impose the local manifold structure of
# the data
X = mat
knn_graph = kneighbors_graph(X, 30, include_self=False)

for connectivity in (None, knn_graph):
    for n_clusters in (30, 3):
        plt.figure(figsize=(10, 4))
        for index, linkage in enumerate(('average', 'complete', 'ward')):
            plt.subplot(1, 3, index + 1)
            model = AgglomerativeClustering(linkage=linkage,
                                            connectivity=connectivity,
                                            n_clusters=n_clusters)
            t0 = time.time()
            model.fit(X)
            elapsed_time = time.time() - t0
            plt.scatter(X[:, 0], X[:, 1], c=model.labels_,
                        cmap=plt.cm.spectral)
            plt.title('linkage=%s (time %.2fs)' % (linkage, elapsed_time),
                      fontdict=dict(verticalalignment='top'))
            plt.axis('equal')
            plt.axis('off')

            plt.subplots_adjust(bottom=0, top=.89, wspace=0,
                                left=0, right=1)
            plt.suptitle('n_cluster=%i, connectivity=%r' %
                         (n_clusters, connectivity is not None), size=17)


plt.show()
