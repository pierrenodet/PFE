## Ajout du chemin vers src pour l'utiliser comme package

import os, sys, inspect
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
cmd_folder = cmd_folder[0:cmd_folder.find("notebooks")]
sys.path.append(cmd_folder)
sys.path.append(cmd_folder+"src/")

## Import des données

import src.make_data

## Preprocessing des données

from src.clean_data import buyer_history

## Data Exploration

#Déjà on peut regarder si les visites sont significatives ou pas :
buyer_history.drop_duplicates().shape[0] - buyer_history[["buyer_id","event","timestamp","status"]].drop_duplicates().shape[0]
#On peut voir que certaines lignes sont redondantes si on enlève les visites. Cela veut dire qu'un personne effectue deux fois la même action au même moment mais avec des visit_id différentes ?
#Ce genre de lignes polluent notre base de données et doivent être enlevées.

#Regardons tout d'abord comment les acheteurs se comportent indépendamment des visites
buyer_history.groupby("buyer_id")["event"].count().describe()
#On peut voir que le nombre d'event median par buyer est de 2 mais que la moyenne est de 6.9 : distribution asymétrique.

#Le nombre d'event max est de 17837 : ce qui est chelou
mec_chelou = buyer_history.groupby("buyer_id")["event"].count().idxmax()
#C'est l'utilisateur mec_chelou, regardons son comportement :
buyer_history[buyer_history["buyer_id"]==mec_chelou]["event"].value_counts()
#On peut voir plus de 10000 page views
((buyer_history["buyer_id"]==mec_chelou) & (buyer_history["event"]=="projet") & (buyer_history["status"]=="Gagné")).sum()
#Seulement 19 projet acheté : C'est peut être le compte d'une entreprise ou simplement d'un employé du magasin réalisant des projets pour ces clients.
#Pour le moment il n'est pas représentatif de la population et peut grandement fausser des futurs résultats : on préfère l'enlever pour le moment.

from src.explore_data import buyer_history

#Regardons de nouveau les acheteurs
buyer_history.groupby("buyer_id")["event"].count().describe()

#On voit que il y a toujours pas mal d'acheteurs qui font beaucoup d'events par rapport à la moyenne : regardons donc le top 20 pour voir s'ils ont un comportement spécial ou pas
#On va regarder leur pageview et leur achat principalement et leur annulation voir s'ils ont hésitants
top20_chelou = buyer_history.groupby("buyer_id")["event"].count().sort_values(ascending=False)[0:19]
for chelou in top20_chelou.index:
    print("pageview = {0}".format(((buyer_history["buyer_id"]==chelou) & (buyer_history["event"]=="pageview")).sum()),end=", ")
    print("achat = {0}".format(((buyer_history["buyer_id"]==chelou) & (buyer_history["event"]=="projet") & (buyer_history["status"]=="Gagné")).sum()),end=", ")
    print("achat = {0}".format(((buyer_history["buyer_id"]==chelou) & (buyer_history["event"]=="projet") & (buyer_history["status"]!="Gagné")).sum()))
#On a l'impression qu'on est face a des acheteurs hésitants plutôt que des données fausses : on va les garder

#Petite info sur le nombre de visite par buyer_id
buyer_history[["buyer_id","visit_id"]].drop_duplicates().groupby(["buyer_id"]).count().describe()

#On va regarder maintenant les timestamps
max_ts = buyer_history[["buyer_id","timestamp"]].groupby(["buyer_id"]).max()
min_ts = buyer_history[["buyer_id","timestamp"]].groupby(["buyer_id"]).min()

from clean_data import stringlist_to_datelist

min_ts["date"]=stringlist_to_datelist(min_ts["timestamp"])
max_ts["date"]=stringlist_to_datelist(max_ts["timestamp"])

#Temps de passage par acheteur
(max_ts["date"]-min_ts["date"]).describe()

#Un petit regard sur les évènements
buyer_history["event"].value_counts()

#evenements + status
buyer_history[["event","status"]].groupby(["event","status"]).size()

#status des projets
buyer_history[buyer_history["event"]=="projet"]["status"].value_counts()

## First model with Density

#Maintenant essayons de calculer les densités d'évenements par rapport au moment de l'achat:
#On importe le dataframe density_data
from model_density import density_data
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
