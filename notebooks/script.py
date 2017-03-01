""" A utliser si problèmes d'import de données
import os, sys, inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
     sys.path.insert(0, cmd_folder)
"""

#Regardons tout d'abord comment les acheteurs se comportent indépendamment des visites
history.groupby("buyer_id")["event"].count().describe()
#On peut voir que le nombre d'event median par buyer est de 2 mais que la moyenne est de 6.9 : distribution asymétrique.

#Le nombre d'event max est de 17837 : ce qui est chelou
mec_chelou = history.groupby("buyer_id")["event"].count().idxmax()
#C'est l'utilisateur mec_chelou, regardons son comportement :
history[history["buyer_id"]==mec_chelou]["event"].value_counts()
#On peut voir plus de 10000 page views
((history["buyer_id"]==mec_chelou) & (history["event"]=="projet") & (history["status"]=="Gagné")).sum()
#Seulement 19 projet acheté : C'est peut être le compte d'une entreprise ou simplement d'un employé du magasin réalisant des projets pour ces clients.
#Pour le moment il n'est pas représentatif de la population et peut grandement fausser des futurs résultats : on préfère l'enlever pour le moment.

#Regardons de nouveau les acheteurs
history.groupby("buyer_id")["event"].count().describe()

#On voit que il y a toujours pas mal d'acheteurs qui font beaucoup d'events par rapport à la moyenne : regardons donc le top 20 pour voir s'ils ont un comportement spécial ou pas
#On va regarder leur pageview et leur achat principalement et leur annulation voir s'ils ont hésitants
top20_chelou = history.groupby("buyer_id")["event"].count().sort_values(ascending=False)[0:19]
for chelou in top20_chelou.index:
    print("pageview = {0}".format(((history["buyer_id"]==chelou) & (history["event"]=="pageview")).sum()),end=", ")
    print("achat = {0}".format(((history["buyer_id"]==chelou) & (history["event"]=="projet") & (history["status"]=="Gagné")).sum()),end=", ")
    print("achat = {0}".format(((history["buyer_id"]==chelou) & (history["event"]=="projet") & (history["status"]!="Gagné")).sum()))
#On a l'impression qu'on est face a des acheteurs hésitants plutôt que des données fausses : on va les garder

#Petite info sur le nombre de visite par buyer_id
history[["buyer_id","visit_id"]].drop_duplicates().groupby(["buyer_id"]).count().describe()

#On va regarder maintenant les timestamps
max_ts = buyer_history[["buyer_id","timestamp"]].groupby(["buyer_id"]).max()
min_ts = buyer_history[["buyer_id","timestamp"]].groupby(["buyer_id"]).min()

min_ts["date"]=stringlist_to_datelist(min_ts["timestamp"])
max_ts["date"]=stringlist_to_datelist(max_ts["timestamp"])

#Temps de passage par acheteur
(max_ts["date"]-min_ts["date"]).describe()

## First model with Density

#Maintenant essayons de calculer les densités d'évenements par rapport au moment de l'achat:
#On importe le dataframe density_data
#Pour calculer la densité on prend donc que les valeures avant le dernier achat de chaque acheteur.
#On calcule donc la difference entre timestamp et last_purchase_timestamp pour cacluler la densité : timestamp_difference
from model_density import density_data

import matplotlib
matplotlib.style.use('ggplot')
import matplotlib.pyplot as plt

#Premier résultat avec des histogrammes stacked
from datetime import timedelta
for event in density["event"].unique():
    (density["time_diff"][density["event"]==event]).apply(timedelta.total_seconds).hist(stacked=True,bins=20).set_xlim(-20000000,0)
plt.show()

#Résultats avec des densités
for event in density["event"].unique():
    (density["time_diff"][density["event"]==event]).apply(timedelta.total_seconds).plot(kind="density",use_index=False).set_xlim(-20000000,0)
plt.show()

#On essaie de réduire le nombre d'event
density.loc[density.loc[:,"event"].apply(str.startswith,args=("crm",)),"event"]="crm"
density.loc[density.loc[:,"event"].apply(str.startswith,args=("iadvize",)),"event"]="iadvize"
density.loc[density.loc[:,"event"].apply(str.startswith,args=("demande",)),"event"]="demande"
density["event"].value_counts()
for event in density["event"].unique():
    (density["time_diff"][density["event"]==event]).apply(timedelta.total_seconds).plot(kind="density",use_index=False).set_xlim(-30000000,0)
plt.show()
#On essaie en enlevant les projets gagnés et les passages en magasin le jour de l'achat
test = density[~((density["event"]=="projet")&(density["status"]=="Gagné"))]
test = test[~((test["event"]=="passage_en_magasin")& (test["time_diff"]==timedelta(minutes=0)))]
#Pour faire un top 5 test["event"].value_counts().index[0:5]:
for event in test["event"].unique():
    (test["time_diff"][test["event"]==event]).apply(timedelta.total_seconds).plot(kind="density",use_index=False,legend='reverse',label=event).set_xlim(-30000000,0)
plt.show()
