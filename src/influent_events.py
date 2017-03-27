from pre_process_data import stringlist_to_datelist
import pandas as pd
from find_dir import cmd_folder

## Import des données

breaks = pd.read_table(cmd_folder+"output/data/breaks.txt",header=None)[0].values
non_buyer_history=pd.read_csv(cmd_folder + "data/interim/non_buyer_history.csv")
buyer_history=pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")
nb_buyer=pd.read_csv(cmd_folder+"data/interim/buyer_history.csv")["buyer_id"].unique().size

## Constructing scoring

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

res = [0]*non_buyer_count["buyer_id"].unique().size
i = 0
for id_nb,non_buyer in non_buyer_count.groupby("buyer_id"):
    score = [0]*(breaks.size)
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
    score[4] = id_nb
    res[i] = score
    i+=1

## Saving score in csv

with open(cmd_folder+"output/data/score.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(res)

## Importing already calculated score

score_non_buyer = pd.read_csv(cmd_folder+"output/data/score.csv",header=None)

id_list = [0]*non_buyer_count["buyer_id"].unique().size
i = 0
for id_nb,non_buyer in non_buyer_count.groupby("buyer_id"):
    id_list[i]=id_nb
    i+=1

score_non_buyer["id"]=id_list

score_non_buyer["cluster"] = score_non_buyer.iloc[:,0:4].apply(lambda x : x.idxmin(),axis=1)+1

clusters_repartition = score_non_buyer["cluster"].value_counts()+nb_buyer

clusters_repartition.to_csv(cmd_folder+'output/data/clusters_repartition.csv',header=None)

## Calculation of influent evenements

drop1 = pd.merge(non_buyer_count,score_non_buyer[score_non_buyer["cluster"]==1],left_on="buyer_id",right_on="id")
keep1 = pd.concat([pd.merge(non_buyer_count,score_non_buyer[((score_non_buyer["cluster"]==2) | (score_non_buyer["cluster"]==3) | (score_non_buyer["cluster"]==4))],left_on="buyer_id",right_on="id"),buyer_count])
drop1["event"].value_counts()/drop1["buyer_id"].unique().size

drop2 = pd.merge(non_buyer_count,score_non_buyer[(score_non_buyer["cluster"]==2)],left_on="buyer_id",right_on="id")
keep2 = pd.concat([pd.merge(non_buyer_count,score_non_buyer[((score_non_buyer["cluster"]==3) | (score_non_buyer["cluster"]==4))],left_on="buyer_id",right_on="id"),buyer_count])

drop3 = pd.merge(non_buyer_count,score_non_buyer[(score_non_buyer["cluster"]==3)],left_on="buyer_id",right_on="id")
keep3 = pd.concat([pd.merge(non_buyer_count,score_non_buyer[((score_non_buyer["cluster"]==4))],left_on="buyer_id",right_on="id"),buyer_count])

drop4 = pd.merge(non_buyer_count,score_non_buyer[(score_non_buyer["cluster"]==4)],left_on="buyer_id",right_on="id")
keep4 = buyer_count.copy()

import matplotlib.pyplot as plt
from numpy import linspace
from matplotlib import cm
colors = [ cm.jet(x) for x in linspace(0.0,1.0, pd.concat([non_buyer_count,buyer_count])["event"].unique().size) ]

plt.gcf().clear()
((((keep1[(keep1["timestamp_percentage"]<breaks[1]) & (pd.isnull(keep1["cluster"]))]["event"].value_counts()\
+ keep1[(keep1["timestamp_percentage"]<breaks[1]/breaks[2]) & (keep1["cluster"]==2)]["event"].value_counts()\
+ keep1[(keep1["timestamp_percentage"]<breaks[1]/breaks[3]) & (keep1["cluster"]==3)]["event"].value_counts()\
+ keep1[(keep1["timestamp_percentage"]<breaks[1]/breaks[4]) & (keep1["cluster"]==4)]["event"].value_counts())\
/ keep1["buyer_id"].unique().size)\
- drop1["event"].value_counts()/drop1["buyer_id"].unique().size)\
/ (drop1["event"].value_counts()/drop1["buyer_id"].unique().size ))\
.plot.bar(color=colors)
plt.savefig(cmd_folder+"output/picture/12.png",bbox_inches='tight')

plt.gcf().clear()
((((keep2[(keep2["timestamp_percentage"]>breaks[1]) & (keep2["timestamp_percentage"]<breaks[2]) & (pd.isnull(keep2["cluster"]))]["event"].value_counts()\
+ keep2[(keep2["timestamp_percentage"]>breaks[1]/breaks[3]) & (keep2["timestamp_percentage"]<breaks[2]/breaks[3]) & (keep2["cluster"]==3)]["event"].value_counts()\
+ keep2[(keep2["timestamp_percentage"]>breaks[1]/breaks[4]) & (keep2["timestamp_percentage"]<breaks[2]/breaks[4]) & (keep2["cluster"]==4)]["event"].value_counts())\
/ keep2["buyer_id"].unique().size)\
- drop2[drop2["timestamp_percentage"]>breaks[1]/breaks[2]]["event"].value_counts()/drop2["buyer_id"].unique().size )\
/ (drop2[drop2["timestamp_percentage"]>breaks[1]/breaks[2]]["event"].value_counts()/drop2["buyer_id"].unique().size ))\
.plot.bar(color=colors)
plt.savefig(cmd_folder+"output/picture/23.png",bbox_inches='tight')

plt.gcf().clear()
((((keep3[(keep3["timestamp_percentage"]>breaks[2]) & (keep3["timestamp_percentage"]<breaks[3]) & (pd.isnull(keep3["cluster"]))]["event"].value_counts()\
+ keep3[(keep3["timestamp_percentage"]>breaks[2]/breaks[4]) & (keep3["timestamp_percentage"]<breaks[3]/breaks[4]) & (keep3["cluster"]==4)]["event"].value_counts())\
/ keep3["buyer_id"].unique().size)\
- drop3[drop3["timestamp_percentage"]>breaks[2]/breaks[3]]["event"].value_counts()/drop3["buyer_id"].unique().size )\
/ (drop3[drop3["timestamp_percentage"]>breaks[2]/breaks[3]]["event"].value_counts()/drop3["buyer_id"].unique().size ))\
.plot.bar(color=colors)
plt.savefig(cmd_folder+"output/picture/34.png",bbox_inches='tight')

plt.gcf().clear()
(((keep4[(keep4["timestamp_percentage"]>breaks[3])]["event"].value_counts()\
/ keep4["buyer_id"].unique().size)\
- drop4[drop4["timestamp_percentage"]>breaks[3]/breaks[4]]["event"].value_counts()/drop4["buyer_id"].unique().size )\
/ (drop4[drop4["timestamp_percentage"]>breaks[3]/breaks[4]]["event"].value_counts()/drop4["buyer_id"].unique().size ))\
.plot.bar(color=colors)
plt.savefig(cmd_folder+"output/picture/4achat.png",bbox_inches='tight')
