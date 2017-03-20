# PARTIE 1 : calcul des matrices de transitions de chaque individu

from find_dir import cmd_folder
import pandas as pd
import json
import numpy as np
import scipy.spatial.distance as ssd
import scipy.cluster.hierarchy as sch
from matplotlib import pyplot as plt

buyer_history = pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")
trace = json.load(open(cmd_folder+"data/processed/trace_regroup.json","r"))


listEvts = []
listEvts.append("start")
listEvts += list(set( buyer_history['event']))
listEvts.append("stop")

transitionMatrix = []

for ind in range(len(trace)):
    mat = np.zeros((len(listEvts), len(listEvts)))
    traceIndiv = trace[ind].get("trace")
    dep = traceIndiv[0].get("event")
    mat[listEvts.index("start")][listEvts.index(dep)] = 1
    arr = dep
    for transition in range(1, len(traceIndiv)):
        arr = traceIndiv[transition].get("event")
        mat[listEvts.index(dep)][listEvts.index(arr)] += 1
        dep=arr
    mat[listEvts.index(arr)][listEvts.index("stop")] = 1  
    transitionMatrix.append({"id":trace[ind].get("id"), "transitionMatrix":mat})

del(dep, arr, ind, mat, transition, traceIndiv)

distanceMatrix = np.zeros((len(transitionMatrix), len(transitionMatrix)))

for ind1 in range(len(transitionMatrix)):
    for ind2 in range(ind1, len(transitionMatrix)):
        dist = np.sqrt(np.sum(np.square(np.array(transitionMatrix[ind1]["transitionMatrix"]) - np.array(transitionMatrix[ind2]["transitionMatrix"]))))
        distanceMatrix[ind1][ind2] = distanceMatrix[ind2][ind1] = dist
del(ind1, ind2, dist)

distArray = ssd.squareform(distanceMatrix)
del(distanceMatrix)

clustering = sch.linkage(distArray, method='average')

plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
sch.dendrogram(
    clustering,
    truncate_mode='lastp',
    p=30,
    show_leaf_counts=True,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
)
plt.axhline(y=17, c='k')
plt.savefig(cmd_folder+"output/picture/dendrogram.png", bbox_inches='tight')
