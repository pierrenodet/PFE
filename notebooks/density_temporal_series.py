## Ajout du chemin vers src pour l'utiliser comme package

import os, sys, inspect
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
cmd_folder = cmd_folder[0:cmd_folder.find("notebooks")]
sys.path.append(cmd_folder)
sys.path.append(cmd_folder+"src/")

from src import buyer_history

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

colors = [ cm.jet(x) for x in linspace(0.0,1.0, density_data_cleaned["event"].unique().size) ]

for i,event in enumerate(density_data_cleaned["event"].unique()):
    (density_data_cleaned["timestamp_difference"][density_data_cleaned["event"]==event]).apply(timedelta.total_seconds).plot(kind="density",use_index=False,legend='reverse',label=event,c=colors[i]).set_xlim(-30000000,0)

plt.legend(loc=2,prop={'size':6})
plt.show()

#On a de bons résultats mais le problème est que les acheteurs ne sont synchronisé que sur la fin des évenements : l'achat final
#On aimerait donc pouvoir les synchronisé au début et à la fin : en utilisant une échelle relative (pourcentage) plutôt qu'une échelle absolue

## Second model : density_perecentage

from src.clean_data import stringlist_to_datelist
import pandas as pd

density_perecentage = buyer_history.copy()

density_perecentage["timestamp"]=stringlist_to_datelist(density_perecentage["timestamp"])

#On recherche le dernier achat par acheteur : groupby et last
last_purchase_timestamp = density_perecentage[["buyer_id","timestamp"]][(density_perecentage["status"]=="Gagné") & (density_perecentage["event"]=="projet")].groupby("buyer_id").max().reset_index()
density_perecentage = pd.merge(density_perecentage,last_purchase_timestamp,on="buyer_id")
density_perecentage.rename(columns={'timestamp_x':'timestamp','timestamp_y':'last_purchase_timestamp'},inplace=True)

#On enlève les évènements arrivant après le dernier achat (sauf si les temps sont égaux)
density_perecentage = density_perecentage[density_perecentage["timestamp"]<=density_perecentage["last_purchase_timestamp"]]

#On cherche la date du premier evenement
first_event_timestamp = density_perecentage[["buyer_id","timestamp"]].groupby("buyer_id").min().reset_index()
density_perecentage = pd.merge(density_perecentage,first_event_timestamp,on="buyer_id")
density_perecentage.rename(columns={'timestamp_x':'timestamp','timestamp_y':'first_event_timestamp'},inplace=True)

#On calcule le pourcentage
density_perecentage["timestamp_difference"]=(density_perecentage["timestamp"]-density_perecentage["first_event_timestamp"])/(density_perecentage["last_purchase_timestamp"]-density_perecentage["first_event_timestamp"])
density_perecentage["timestamp_difference"].describe()

#On plot
from matplotlib import cm
from numpy import linspace
from datetime import timedelta

#Par evenement
colors = [ cm.jet(x) for x in linspace(0.0,1.0, density_perecentage["event"].unique().size) ]

for i,event in enumerate(density_perecentage["event"].unique()):
    (density_perecentage["timestamp_difference"][density_perecentage["event"]==event]).plot(kind="density",use_index=False,legend='reverse',label=event,figsize=(20,20),c=colors[i]).set_xlim(0,1)

plt.legend(loc=2,prop={'size':6})
plt.show()

#Avec certains évenements
density_perecentage.loc[density_perecentage.loc[:,"event"].apply(str.startswith,args=("crm",)),"event"]="crm"
density_perecentage.loc[density_perecentage.loc[:,"event"].apply(str.startswith,args=("iadvize",)),"event"]="iadvize"
density_perecentage.loc[density_perecentage.loc[:,"event"].apply(str.startswith,args=("demande",)),"event"]="demande"

colors = [ cm.jet(x) for x in linspace(0.0,1.0, density_perecentage["event"].unique().size) ]

for i,event in enumerate(density_perecentage["event"].unique()):
    (density_perecentage["timestamp_difference"][density_perecentage["event"]==event]).plot(kind="density",use_index=False,legend='reverse',label=event,figsize=(20,20),c=colors[i]).set_xlim(0,1)

plt.legend(loc=2,prop={'size':30})
plt.show()

#Stacked
(density_perecentage["timestamp_difference"]).plot(kind="density",use_index=False,legend='reverse',label=event,figsize=(20,20)).set_xlim(0,1)
plt.show()
