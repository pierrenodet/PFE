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

#Petite info sur le nombre de visite par buyer_id
history[["buyer_id","visit_id"]].drop_duplicates().groupby(["buyer_id"]).count().describe()

#On va regarder maintenant les timestamps
max_ts = history[["buyer_id","timestamp"]].groupby(["buyer_id"]).max()
min_ts = history[["buyer_id","timestamp"]].groupby(["buyer_id"]).min()

from datetime import datetime

def string_to_date(input_list):
    kek=[0]*input_list.size
    for i,m in enumerate(input_list):
        kek[i] = datetime.strptime(m.split(".")[0],"%Y-%m-%d %H:%M:%S")
    return kek

min_ts["date"]=string_to_date(min_ts["timestamp"])
max_ts["date"]=string_to_date(max_ts["timestamp"])

#Temps de passage par acheteur
(max_ts["date"]-min_ts["date"]).describe()

#Maintenant essayons de calculer les densités d'évenements par rapport au moment de l'achat:
#On crée un nouveau dataframe en changeant bien le type du timestamp
density=history.copy()
density["timestamp"]=string_to_date(density["timestamp"])
#density = pd.merge(density,max_ts.reset_index()[["buyer_id","date"]],on="buyer_id")
#density=density.rename(columns = {'date_x':'min','date_y':'max'})
#Ici on récupère la valuer du timestamp pour chaque achat ; puis on fait un groupby par buyer_id et on prend le timestamp du dernier achat (max)
density = pd.merge(density,density[["buyer_id","timestamp"]][(density["status"]=="Gagné") & (density["event"]=="projet")].groupby("buyer_id").last().reset_index(),on="buyer_id")
density.rename(columns={'timestamp_x':'timestamp','timestamp_y':'dernier_achat'},inplace=True)
#Pour calculer la densité on prend donc que les valeures avant ce dernier achat.
density = density[density["timestamp"]<=density["dernier_achat"]]
#On calcule donc la difference entre timestamp et dernier_achat pour cacluler la densité
density["time_diff"]=density["timestamp"]-density["dernier_achat"]
from datetime import timedelta
for event in density["event"].unique():
    (density["time_diff"][density["event"]==event]).apply(timedelta.total_seconds).hist(stacked=True,bins=20).set_xlim(-20000000,0)

import matplotlib
matplotlib.style.use('ggplot')
import matplotlib.pyplot as plt
plt.show()

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
#On essaie le top 5
for event in density["event"].value_counts().index[0:5]:
    (density["time_diff"][density["event"]==event]).apply(timedelta.total_seconds).plot(kind="density",use_index=False).set_xlim(-30000000,0)
plt.show()
