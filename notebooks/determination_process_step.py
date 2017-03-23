from clean_data import stringlist_to_datelist
import pandas as pd
from find_dir import cmd_folder

## Import des données

breaks = pd.read_table(cmd_folder+"output/data/breaks.txt",header=None)[0].values
non_buyer_history=pd.read_csv(cmd_folder + "data/interim/non_buyer_history.csv")
buyer_history=pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")

## Statistique exploratoire pour les non acheteurs

non_buyer_history.groupby("buyer_id").size().describe()

import matplotlib.pyplot as plt

non_buyer_history.drop(pd.merge(non_buyer_history, pd.DataFrame(non_buyer_history.groupby("buyer_id")["event"].count().sort_values(ascending=False)[0:7].index), on=["buyer_id"],right_index=True).index,inplace=True)

non_buyer_history.groupby("buyer_id")["event"].count().plot(kind="box")
plt.show()

non_buyer_history["event"].value_counts()

## Calcul de la densité percentage pour les non acheteurs

def limit_timestamp(arg,data_history):
    timestamp = getattr(data_history[["buyer_id","timestamp"]].groupby("buyer_id"),arg)().reset_index()
    data_history = pd.merge(data_history,timestamp,on="buyer_id")
    data_history.rename(columns={'timestamp_x':'timestamp','timestamp_y':arg+'_timestamp'},inplace=True)
    return data_history

def init_count(data_history):
    data_count = data_history.copy()

    data_count.drop("visit_id",axis=1,inplace=True)
    data_count["timestamp"]=stringlist_to_datelist(data_count["timestamp"])

    data_count = limit_timestamp("min",data_count)
    data_count = limit_timestamp("max",data_count)

    data_count["timestamp_percentage"]=(data_count["timestamp"]-data_count["min_timestamp"])/(data_count["max_timestamp"]-data_count["min_timestamp"])
    return data_count

non_buyer_count = init_count(non_buyer_history)
buyer_count = init_count(buyer_history)

step=[0]*(breaks.size-1)
for i in range(breaks.size-1):
    step[i] = buyer_count[(buyer_count["timestamp_percentage"]>=breaks[i]) & (buyer_count["timestamp_percentage"]<breaks[i+1])].groupby(["event"]).count()["buyer_id"]
    step[i] = step[i] / buyer_count[(buyer_count["timestamp_percentage"]>=breaks[i]) & (buyer_count["timestamp_percentage"]<breaks[i+1])]["buyer_id"].unique().size
    #step[i] = step[i] / step[i].sum()

id_test = non_buyer_count["buyer_id"].unique()[95000:96000]
test_count = pd.merge(non_buyer_count,pd.DataFrame(id_test,columns=["buyer_id"]),on="buyer_id")

#(pd.DataFrame(test_count.groupby(["buyer_id","event"]).count()["timestamp"])/pd.DataFrame(test_count.groupby(["buyer_id","event"]).count()["timestamp"]).sum(level=[0])).reset_index(["event"]).apply(diff)

#for rows in pd.DataFrame(test_count.groupby(["buyer_id","event"]).count()["timestamp"]).itertuples():
#    print(test_count[test_count["buyer_id"]==rows[0][0]])

#for id_nb, non_buyer in pd.DataFrame(test_count.groupby(["buyer_id","event"]).count()["timestamp"]).groupby(level=0):
#        print(non_buyer)

import numpy

res = [0]*test_count["buyer_id"].unique().size
i = 0
for id_nb,non_buyer in test_count.groupby("buyer_id"):
    score = [0]*(breaks.size-1)
    score[0] = (step[0].subtract(non_buyer["event"].value_counts(),fill_value=0)**2).sum()
    score[1] = (step[0].subtract(non_buyer[non_buyer["timestamp_percentage"]<(breaks[1]/breaks[2])]["event"].value_counts(),fill_value=0)**2).sum()\
    + (step[1].subtract(non_buyer[non_buyer["timestamp_percentage"]>=(breaks[1]/breaks[2])]["event"].value_counts(),fill_value=0)**2).sum()
    score[2] = (step[0].subtract(non_buyer[non_buyer["timestamp_percentage"]<(breaks[1]/breaks[3])]["event"].value_counts(),fill_value=0)**2).sum()\
    + (step[1].subtract(non_buyer[(non_buyer["timestamp_percentage"]>=(breaks[1]/breaks[3])) & (non_buyer["timestamp_percentage"]<(breaks[2]/breaks[3]))]["event"].value_counts(),fill_value=0)**2).sum() \
    + (step[2].subtract(non_buyer[non_buyer["timestamp_percentage"]>=(breaks[2]/breaks[3])]["event"].value_counts(),fill_value=0)**2).sum()
    score[3] = (step[0].subtract(non_buyer[non_buyer["timestamp_percentage"]<(breaks[1]/breaks[4])]["event"].value_counts(),fill_value=0)**2).sum()\
    + (step[1].subtract(non_buyer[(non_buyer["timestamp_percentage"]>=(breaks[1]/breaks[4])) & (non_buyer["timestamp_percentage"]<(breaks[2]/breaks[4]))]["event"].value_counts(),fill_value=0)**2).sum() \
    + (step[2].subtract(non_buyer[(non_buyer["timestamp_percentage"]>=(breaks[1]/breaks[4])) & (non_buyer["timestamp_percentage"]<(breaks[2]/breaks[4]))]["event"].value_counts(),fill_value=0)**2).sum() \
    + (step[3].subtract(non_buyer[non_buyer["timestamp_percentage"]>=(breaks[3]/breaks[4])]["event"].value_counts(),fill_value=0)**2).sum()
    res[i] = score
    i+=1

kek = [0]*len(res)
for i,r in enumerate(res):
    kek[i] = r.index(min(r))

pd.Series(kek).value_counts()

res = [0]*non_buyer_count["buyer_id"].unique().size
i = 0
for id_nb,non_buyer in non_buyer_count.groupby("buyer_id"):
    score = [0]*(breaks.size-1)
    score[0] = (step[0].subtract(non_buyer["event"].value_counts(),fill_value=0)**2).sum()
    score[1] = (step[0].subtract(non_buyer[non_buyer["timestamp_percentage"]<(breaks[1]/breaks[2])]["event"].value_counts(),fill_value=0)**2).sum()\
    + (step[1].subtract(non_buyer[non_buyer["timestamp_percentage"]>=(breaks[1]/breaks[2])]["event"].value_counts(),fill_value=0)**2).sum()
    score[2] = (step[0].subtract(non_buyer[non_buyer["timestamp_percentage"]<(breaks[1]/breaks[3])]["event"].value_counts(),fill_value=0)**2).sum()\
    + (step[1].subtract(non_buyer[(non_buyer["timestamp_percentage"]>=(breaks[1]/breaks[3])) & (non_buyer["timestamp_percentage"]<(breaks[2]/breaks[3]))]["event"].value_counts(),fill_value=0)**2).sum() \
    + (step[2].subtract(non_buyer[non_buyer["timestamp_percentage"]>=(breaks[2]/breaks[3])]["event"].value_counts(),fill_value=0)**2).sum()
    score[3] = (step[0].subtract(non_buyer[non_buyer["timestamp_percentage"]<(breaks[1]/breaks[4])]["event"].value_counts(),fill_value=0)**2).sum()\
    + (step[1].subtract(non_buyer[(non_buyer["timestamp_percentage"]>=(breaks[1]/breaks[4])) & (non_buyer["timestamp_percentage"]<(breaks[2]/breaks[4]))]["event"].value_counts(),fill_value=0)**2).sum() \
    + (step[2].subtract(non_buyer[(non_buyer["timestamp_percentage"]>=(breaks[1]/breaks[4])) & (non_buyer["timestamp_percentage"]<(breaks[2]/breaks[4]))]["event"].value_counts(),fill_value=0)**2).sum() \
    + (step[3].subtract(non_buyer[non_buyer["timestamp_percentage"]>=(breaks[3]/breaks[4])]["event"].value_counts(),fill_value=0)**2).sum()
    res[i] = score
    i+=1

kek = [0]*len(res)
for i,r in enumerate(res):
    kek[i] = r.index(min(r))

pd.Series(kek).value_counts()

import csv

with open(cmd_folder+"output/data/score.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(res)

















from numpy import linspace
from scipy.stats import gaussian_kde

xs=linspace(0,1,1000)
kernels=[[]*xs.size]*non_buyer_count["event"].unique().size
for i,event in enumerate(non_buyer_count["event"].unique()):
    kernels[i] = gaussian_kde(density_percentage["timestamp_percentage"][density_percentage["event"]==event].dropna())(xs)

from matplotlib import cm

colors = [ cm.jet(x) for x in linspace(0.0,1.0, density_percentage["event"].unique().size) ]

plt.gcf().clear()
plt.figure(figsize=(10,8))

for i,event in enumerate(density_percentage["event"].unique()):
    plt.plot(xs,kernels[i],c=colors[i],label=event)


plt.legend(loc=2,prop={'size':6})
plt.show()





kek = density_percentage["buyer_id"][0]
kek2 = density_percentage[density_percentage["buyer_id"]==kek]

plt.gcf().clear()

kekrnels=[[]*xs.size]*density_percentage["event"].unique().size
for i,event in enumerate(density_percentage["event"].unique()):
    if kek2[kek2["event"]==event].size>1:
        kekrnels[i] = gaussian_kde(kek2["timestamp_percentage"][kek2["event"]==event].dropna())(xs)

for i,event in enumerate(density_percentage["event"].unique()):
    if kek2[kek2["event"]==event].size>1:
        plt.plot(xs,kekrnels[i],c=colors[i],label=event)

plt.legend(loc=2,prop={'size':6})
plt.show()
