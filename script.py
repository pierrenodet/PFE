##Importing Config File

import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

data_dir = cfg['paths']['data_dir']

##Importing Data

import pandas as pd

history=pd.read_csv(data_dir + "export_ensai_buyersHistory_170216.csv",sep="\t",header=None)
history.columns=["buyer_id","visit_id","timestamp","event","status"]

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
history = history[history["buyer_id"]!=mec_chelou].reset_index(drop=True)

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
