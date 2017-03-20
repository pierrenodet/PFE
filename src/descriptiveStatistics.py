#Descriptive statistics of the initial data
from find_dir import cmd_folder
import matplotlib.pyplot as plt
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
plt.show()

buyer_history["buyer_id"].value_counts().value_counts()[1]
buyer_history["buyer_id"].value_counts().value_counts()[2]
buyer_history["buyer_id"].value_counts().value_counts()[3]
8731/(11+8731+2196) #80% des parcours courts n'ont que 3 evts

buyer_history = pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")
len(set(buyer_history["buyer_id"]))
buyer_history["event"].value_counts() # occurences of each event after keeping only the 3092 buyers 
                    # with more than 3 events and more than one day between their firt and last event


#non buyers descriptive statistics
non_buyer_history["buyer_id"].value_counts().describe()

non_buyer_history.drop(pd.merge(non_buyer_history, pd.DataFrame(non_buyer_history.groupby("buyer_id")["event"].count().sort_values(ascending=False)[0:1].index), on=["buyer_id"],right_index=True).index,inplace=True)
plt.figure(figsize=(15, 1))
plt.boxplot(non_buyer_history["buyer_id"].value_counts(), vert = 0, sym = 'b.')
plt.show()

non_buyer_history.drop(pd.merge(non_buyer_history, pd.DataFrame(non_buyer_history.groupby("buyer_id")["event"].count().sort_values(ascending=False)[0:7].index), on=["buyer_id"],right_index=True).index,inplace=True)

len(set(non_buyer_history["buyer_id"])) #nb of non buyers after cleaning

non_buyer_history["event"].value_counts()