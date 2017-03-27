import pandas as pd
from datetime import timedelta
from find_dir import cmd_folder
from clean_data import stringlist_to_datelist

from numpy import linspace
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from matplotlib import cm

##Importing data

buyer_history=pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")

##Important steps of modeling density

density_difference = buyer_history.copy()

density_difference.drop("visit_id",axis=1,inplace=True)
density_difference["timestamp"]=stringlist_to_datelist(density_difference["timestamp"])

last_purchase_timestamp = density_difference[["buyer_id","timestamp"]][density_difference["event"]=="project_win"].groupby("buyer_id").max().reset_index()
density_difference = pd.merge(density_difference,last_purchase_timestamp,on="buyer_id")
density_difference.rename(columns={'timestamp_x':'timestamp','timestamp_y':'last_purchase_timestamp'},inplace=True)

density_difference = density_difference[density_difference["timestamp"]<=density_difference["last_purchase_timestamp"]]

density_percentage = density_difference.copy()

density_difference.loc[:,"timestamp_difference"]=(density_difference["timestamp"]-density_difference["last_purchase_timestamp"]).apply(timedelta.total_seconds)

density_difference.drop(density_difference[density_difference["event"]=="quote_lose"].index.values,inplace=True)

density_difference.to_csv(cmd_folder+"data/interim/density_difference.csv",index=False)

first_event_timestamp = density_percentage[["buyer_id","timestamp"]].groupby("buyer_id").min().reset_index()
density_percentage = pd.merge(density_percentage,first_event_timestamp,on="buyer_id")
density_percentage.rename(columns={'timestamp_x':'timestamp','timestamp_y':'first_event_timestamp'},inplace=True)

density_percentage["timestamp_percentage"]=(density_percentage["timestamp"]-density_percentage["first_event_timestamp"])/(density_percentage["last_purchase_timestamp"]-density_percentage["first_event_timestamp"])

density_percentage.drop(density_percentage[density_percentage["event"]=="quote_lose"].index.values,inplace=True)

density_percentage.to_csv(cmd_folder+"data/processed/density_percentage.csv",index=False)

xs=linspace(0,1,1000)
kernels=[[]*xs.size]*density_percentage["event"].unique().size
for i,event in enumerate(density_percentage["event"].unique()):
    kernels[i] = gaussian_kde(density_percentage["timestamp_percentage"][density_percentage["event"]==event].dropna())(xs)

max_events = [0]*xs.size
for x in range(xs.size):
    maxi=0
    for i in range(density_percentage["event"].unique().size):
        if maxi < kernels[i][x]:
            maxi = kernels[i][x]
            max_events[x] = density_percentage["event"].unique()[i]

max_event = max_events[0]
breaks = [0]
limit = 0
for x in range(xs.size):
    limit +=1
    if max_event != max_events[x]:
        if limit > xs.size*0.2:
            limit = 0
            max_event = max_events[x]
            breaks.append(x)
        else:
            max_event = max_events[x]
breaks.append(xs.size)

colors = [ cm.jet(x) for x in linspace(0.0,1.0, density_percentage["event"].unique().size) ]

with open(cmd_folder+"output/data/breaks.txt",'w') as breaks_file:
    breaks_file.write('\n'.join(str(b/xs.size) for b in breaks))

plt.gcf().clear()
plt.figure(figsize=(16,10))
for i,event in enumerate(density_percentage["event"].unique()):
    (density_percentage["timestamp_percentage"][density_percentage["event"]==event]).hist(stacked=True,bins=20,color=colors[i],label=event).set_xlim(0,1)
plt.legend(prop={'size':6})
plt.savefig(cmd_folder+"output/picture/hist.png",bbox_inches='tight')

plt.gcf().clear()
plt.figure(figsize=(16,10))
plt.stackplot(xs,kernels,colors=colors)
plt.legend(density_percentage["event"].unique(),prop={'size':6})
plt.savefig(cmd_folder+"output/picture/density_stacked.png",bbox_inches='tight')

plt.gcf().clear()
plt.figure(figsize=(16,10))
for i,event in enumerate(density_percentage["event"].unique()):
    plt.plot(xs,kernels[i],c=colors[i],label=event)
plt.legend(loc=2,prop={'size':6})
plt.savefig(cmd_folder+"output/picture/density.png",bbox_inches='tight')

plt.gcf().clear()
plt.figure(figsize=(16,10))
for i,event in enumerate(density_percentage["event"].unique()):
    plt.plot(xs,kernels[i],c=colors[i],label=event)
plt.legend(loc=2,prop={'size':6})
for b in breaks[1:len(breaks)]:
    plt.axvline(b/xs.size,linestyle="--")
plt.savefig(cmd_folder+"output/picture/density_breaks.png",bbox_inches='tight')
