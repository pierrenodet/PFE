import pandas as pd
from datetime import datetime
from find_dir import cmd_folder

##Importing Data

history=pd.read_csv(cmd_folder + "data/raw/export_ensai_history_170307170002.csv",sep="\t",header=None)

##Cleaning Data

history.columns=["buyer_id","visit_id","timestamp","event","status"]

def stringlist_to_datelist(stringlist):
    datelist=[0]*stringlist.size
    for i,string in enumerate(stringlist):
        datelist[i] = datetime.strptime(string.split(".")[0],"%Y-%m-%d %H:%M:%S")
    return datelist

history["timestamp"]=stringlist_to_datelist(history["timestamp"])

history.drop_duplicates(inplace=True)

group=pd.read_excel(cmd_folder+"data/raw/PFEensai2017_description_des_donnees.xlsx")
group.rename(columns={'event_name':'event','group_name':'group'},inplace=True)
history.loc[:,"event"]=history[["event","status"]].reset_index().merge(group,on=["event","status"]).set_index('index')["group"]
history.drop("status",axis=1,inplace=True)

non_buyer_history = pd.DataFrame(columns=["buyer_id","visit_id","timestamp","event"])
buyer_history = pd.DataFrame(columns=["buyer_id","visit_id","timestamp","event"])

buyer_history = pd.merge(history,pd.DataFrame(history[history["event"]=="project_win"]["buyer_id"].values,columns=["buyer_id"]),how="inner",on="buyer_id",right_index=True)

non_buyer_history = history.drop(buyer_history.index)

non_buyer_history.to_csv(cmd_folder+"data/interim/non_buyer_history.csv",index=False)

buyer_history.to_csv(cmd_folder+"data/interim/buyer_history.csv",index=False)


#buyer_history=pd.read_csv(cmd_folder + "data/raw/export_ensai_buyersHistory_170216.csv",sep="\t",header=None)
