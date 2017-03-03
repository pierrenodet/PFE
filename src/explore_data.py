import pandas as pd
from find_dir import cmd_folder

## Important modifications of data resulting from exploration

buyer_history=pd.read_csv(cmd_folder+"data/interim/buyer_history_noduplicate.csv")

buyer_history = buyer_history.loc[list(buyer_history.loc[:,["buyer_id","timestamp","event"]].drop_duplicates().index),:]

mec_chelou = buyer_history.groupby("buyer_id")["event"].count().idxmax()
buyer_history = buyer_history[buyer_history["buyer_id"]!=mec_chelou].reset_index(drop=True)

group=pd.read_excel(cmd_folder+"data/raw/PFEensai2017_description_des_donnees.xlsx")
group.rename(columns={'event_name':'event','group_name':'group'},inplace=True)
buyer_history.loc[:,"event"]=buyer_history[["event","status"]].reset_index().merge(group,on=["event","status"]).set_index('index')["group"]
buyer_history.drop("status",axis=1,inplace=True)

buyer_history.to_csv(cmd_folder+"data/processed/buyer_history.csv",index=False)
