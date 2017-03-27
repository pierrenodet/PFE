#Descriptive statistics of the initial data
from find_dir import cmd_folder
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd

buyer_history = pd.read_csv(cmd_folder+"data/interim/buyer_history.csv")
non_buyer_history = pd.read_csv(cmd_folder+"data/interim/non_buyer_history.csv")

len(buyer_history) + len(non_buyer_history) #initial nb of logs

buyer_history = buyer_history.loc[list(buyer_history.loc[:,["buyer_id","timestamp","event"]].drop_duplicates().index),:]
non_buyer_history = non_buyer_history.loc[list(non_buyer_history.loc[:,["buyer_id","timestamp","event"]].drop_duplicates().index),:]

len(set(buyer_history["buyer_id"])) #nb of buyers
len(set(non_buyer_history["buyer_id"])) #nb of non buyers


#buyers descriptive statistics
buyer_history["buyer_id"].value_counts().describe()

buyer_history.drop(pd.merge(buyer_history, pd.DataFrame(buyer_history.groupby("buyer_id")["event"].count().sort_values(ascending=False)[0:1].index), on=["buyer_id"],right_index=True).index,inplace=True)
plt.figure(figsize=(15, 1))
plt.boxplot(buyer_history["buyer_id"].value_counts(), vert = 0, sym = 'b.')
plt.savefig(cmd_folder+"output/picture/boxplotBuyers.png", bbox_inches='tight')

len_trace = buyer_history.groupby("buyer_id").size()
short_buyer_history = pd.merge(buyer_history,pd.DataFrame(len_trace[len_trace<4].index),on="buyer_id",how="inner")
short_buyer_history.groupby("buyer_id").size().value_counts()
short_buyer_history.groupby("buyer_id").size().value_counts()[2]/sum(short_buyer_history.groupby("buyer_id").size().value_counts()) #80% des parcours courts n'ont que 3 evts

event_count = short_buyer_history["event"].value_counts()
event_count["events with less than 500 occurences"]=sum(event_count[event_count < 500])
event_count = event_count[event_count >= 500]
plt.figure(figsize=(5, 5))
plt.pie(event_count, labels=event_count.index, colors=("#2c4caa", "#536283","#98a5c1","#94e1e3","#def1f9"), autopct='%1.1f%%')
plt.savefig(cmd_folder+"output/picture/piechart.svg", bbox_inches='tight')

buyer_history = pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")
len(set(buyer_history["buyer_id"]))
buyer_history["event"].value_counts() # occurences of each event after keeping only the 3092 buyers 
                    # with more than 3 events and more than one day between their firt and last event

r=range(22)
plt.figure(figsize=(8, 5))
plt.barh(r, buyer_history["event"].value_counts())
plt.yticks([r + 0.5 for r in range(22)], buyer_history["event"].value_counts().index)
plt.savefig(cmd_folder+"output/picture/buyersEventCount.png", bbox_inches='tight')


#non buyers descriptive statistics
non_buyer_history["buyer_id"].value_counts().describe()

non_buyer_history.drop(pd.merge(non_buyer_history, pd.DataFrame(non_buyer_history.groupby("buyer_id")["event"].count().sort_values(ascending=False)[0:1].index), on=["buyer_id"],right_index=True).index,inplace=True)
plt.figure(figsize=(15, 1))
plt.boxplot(non_buyer_history["buyer_id"].value_counts(), vert = 0, sym = 'b.')
plt.savefig(cmd_folder+"output/picture/boxplotNonBuyers.png", bbox_inches='tight')

non_buyer_history.drop(pd.merge(non_buyer_history, pd.DataFrame(non_buyer_history.groupby("buyer_id")["event"].count().sort_values(ascending=False)[0:7].index), on=["buyer_id"],right_index=True).index,inplace=True)

len(set(non_buyer_history["buyer_id"])) #nb of non buyers after cleaning

non_buyer_history["event"].value_counts()