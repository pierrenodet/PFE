import pandas as pd
from datetime import datetime
from find_dir import cmd_folder

##Importing Data

buyer_history=pd.read_csv(cmd_folder + "data/raw/export_ensai_buyersHistory_170216.csv",sep="\t",header=None)

##Cleaning Data

buyer_history.columns=["buyer_id","visit_id","timestamp","event","status"]

def stringlist_to_datelist(stringlist):
    datelist=[0]*stringlist.size
    for i,string in enumerate(stringlist):
        datelist[i] = datetime.strptime(string.split(".")[0],"%Y-%m-%d %H:%M:%S")
    return datelist

buyer_history["timestamp"]=stringlist_to_datelist(buyer_history["timestamp"])

buyer_history.drop_duplicates(inplace=True)

buyer_history.to_csv(cmd_folder+"data/interim/buyer_history_noduplicate.csv",index=False)
