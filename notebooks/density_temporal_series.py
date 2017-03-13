## Ajout du chemin vers src pour l'utiliser comme package

import os, sys, inspect
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
cmd_folder = cmd_folder[0:cmd_folder.find("notebooks")]
sys.path.append(cmd_folder)
sys.path.append(cmd_folder+"src/")

## First model with Density

#Maintenant essayons de calculer les densités d'évenements par rapport au moment de l'achat:
#On importe le dataframe density_data
from src.model_density import density_data
#Pour calculer la densité on prend donc que les valeures avant le dernier achat de chaque acheteur.

#On calcule donc la difference entre timestamp et last_purchase_timestamp pour cacluler la densité : timestamp_difference
import matplotlib.pyplot as plt
plt.style.use('ggplot')

#Premier résultat avec des histogrammes stacked
for event in density_data["event"].unique():
    (density_data["timestamp_difference"][density_data["event"]==event]).apply(timedelta.total_seconds).hist(stacked=True,bins=20).set_xlim(-20000000,0)
plt.show()

#Le nombre d'évenements différents est trop important pour tout étudier comme ça, on regroupe les "crm", les "iadvize" et les "demande" ensemble.
#On retire aussi les évenements qui sont évidents tel que l'achat du projet et le passage en magasin le jour J.

from src.model_density import density_data_cleaned

#Résultats avec des densités
from matplotlib import cm
from numpy import linspace


colors = [ cm.jet(x) for x in linspace(0.0,1.0, density_data_cleaned["group"].unique().size) ]

for i,event in enumerate(density_data_cleaned["group"].unique()):
    (density_data_cleaned["timestamp_difference"][density_data_cleaned["group"]==event]).apply(timedelta.total_seconds).plot(kind="density",use_index=False,legend='reverse',label=event,c=colors[i]).set_xlim(-30000000,0)

plt.legend(loc=2,prop={'size':6})
plt.show()

#On a de bons résultats mais le problème est que les acheteurs ne sont synchronisé que sur la fin des évenements : l'achat final
#On aimerait donc pouvoir les synchronisé au début et à la fin : en utilisant une échelle relative (pourcentage) plutôt qu'une échelle absolue

## Second model : density_perecentage

from src.clean_data import stringlist_to_datelist
import pandas as pd

from src.model_density import density_percentage

#On plot
from matplotlib import cm
from numpy import linspace
from datetime import timedelta

#Par evenement
colors = [ cm.jet(x) for x in linspace(0.0,1.0, density_percentage["event"].unique().size) ]

for i,event in enumerate(density_percentage["event"].unique()):
    (density_percentage["timestamp_percentage"][density_percentage["event"]==event]).plot(kind="density",use_index=False,legend='reverse',label=event,figsize=(10,8),c=colors[i]).set_xlim(0,1)

plt.legend(loc=2,prop={'size':6})
plt.show()

#Stacked
(density_percentage["timestamp_percentage"]).plot(kind="density",use_index=False,legend='reverse',label=event,figsize=(15,5)).set_xlim(0,1)
plt.show()

from scipy.stats import gaussian_kde
colors = [ cm.jet(x) for x in linspace(0.0,1.0, density_percentage["event"].unique().size) ]
xs=linspace(0,1,200)

#Stacked avec repartition
kernel=[0]*density_percentage["event"].unique().size
for i,event in enumerate(density_percentage["event"].unique()):
    kernel[i] = gaussian_kde(density_percentage["timestamp_percentage"][density_percentage["event"]==event].dropna())(xs)
plt.stackplot(xs,kernel,colors=colors)
plt.legend(density_percentage["event"].unique(),prop={'size':4})
plt.show()

#Calcul du rapport entre densité de l'évenement et densité de tous les evenements
kernel=[0]*density_percentage["event"].unique().size
for i,event in enumerate(density_percentage["event"].unique()):
    kernel[i] = gaussian_kde(density_percentage["timestamp_percentage"][density_percentage["event"]==event].dropna())(xs)/gaussian_kde(density_percentage["timestamp_percentage"].dropna())(xs)
plt.stackplot(xs,kernel,colors=colors)
plt.legend(density_percentage["event"].unique(),prop={'size':6})
plt.show()

import matplotlib.pyplot as plt
from matplotlib import cm
from numpy import linspace
from scipy.stats import gaussian_kde

#Par evenement
colors = [ cm.jet(x) for x in linspace(0.0,1.0, density_percentage["event"].unique().size) ]
xs=linspace(0,1,1000)
kernels=[0]*xs.size
for i,event in enumerate(density_percentage["event"].unique()):
    kernels = kernels + gaussian_kde(density_percentage["timestamp_percentage"][density_percentage["event"]==event].dropna())(xs)/gaussian_kde(density_percentage["timestamp_percentage"].dropna())(xs)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import math

def online(X,y,threshold):
    start = 0
    res = []
    score = 0
    param = 0
    for i in range(1,X.size):
        reg = LinearRegression().fit(X[start:i],y[start:i])
        mse = mean_squared_error(reg.predict(X[start:i]),y[start:i])
        if mse > threshold:
            start = i
            res.append(i/X.size)
            score = score - N/2*math.log(2*math.pi) -  mse
            param +=2
    return res,score,param

def online_cusum(X,y,threshold):
    start = 0
    res = []
    cusum = 0
    score = 0
    param = 0
    for i in range(1,X.size):
        reg = LinearRegression().fit(X[start:i],y[start:i])
        mse = mean_squared_error(reg.predict(X[start:i]),y[start:i])
        cusum = cusum + mse
        if cusum > threshold:
            start = i
            cusum = 0
            score = score + mse
            res.append(i/X.size)
            param += 2
    return res,score,param


normal,n_score,n_param = online(xs.reshape(-1,1),kernels.reshape(-1,1),1)
cusum,c_score,c_param = online_cusum(xs.reshape(-1,1),kernels.reshape(-1,1),50)

opt_score = 10000
opt_param =

for k in range(0.01,2,0.01):

    if
    normal,n_score,n_param = online(xs.reshape(-1,1),kernels.reshape(-1,1),k)


cusum,c_score,c_param = online_cusum(xs.reshape(-1,1),kernels.reshape(-1,1),50)


plt.plot(xs,kernels,color=colors[0])
for n in normal:
    ln = plt.axvline(n,linestyle="--",color=colors[2])
for c in cusum:
    lc = plt.axvline(c,linestyle="--",color=colors[8])
plt.legend((ln,lc),("normal","cusum"))
plt.show()

xs=linspace(0,1,1000)

kernel=[0]*density_percentage["event"].unique().size
for i,event in enumerate(density_percentage["event"].unique()):
    kernel[i] = gaussian_kde(density_percentage["timestamp_percentage"][density_percentage["event"]==event].dropna())(xs)

event = [0]*xs.size
for x in range(xs.size):
    maxi=0
    for i in range(density_percentage["event"].unique().size):
        if maxi < kernel[i][x]:
            maxi = kernel[i][x]
            event[x] = density_percentage["event"].unique()[i]

test = event[0]
breaks = []
x = 0
limit = 0
for x in range(xs.size):
    limit +=1
    if (test != event[x]) & (limit > xs.size*0.2):
        limit = 0
        test = event[x]
        breaks.append(x)
    if (test != event[x]) & ~(limit > xs.size*0.2):
        test = event[x]

breaks
xs.size
