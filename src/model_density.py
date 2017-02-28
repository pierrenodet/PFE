import pandas as pd
from datetime import datetime
from datetime import timedelta
from find_dir import cmd_folder
from clean_data import stringlist_to_datelist

##Importing data

buyer_history=pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")

##Important steps of modeling density

density_data = buyer_history.copy()

density_data["timestamp"]=stringlist_to_datelist(density_data["timestamp"])

last_purchase_timestamp = density_data[["buyer_id","timestamp"]][(density_data["status"]=="Gagné") & (density_data["event"]=="projet")].groupby("buyer_id").last().reset_index()
density_data = pd.merge(density_data,last_purchase_timestamp,on="buyer_id")
density_data.rename(columns={'timestamp_x':'timestamp','timestamp_y':'last_purchase_timestamp'},inplace=True)

density_data = density_data[density_data["timestamp"]<=density_data["last_purchase_timestamp"]]
density_data["timestamp_difference"]=density_data["timestamp"]-density_data["last_purchase_timestamp"]

density_data.to_csv(cmd_folder+"data/interim/density_data.csv",index=False)

density_data_cleaned = density_data[~((density_data["event"]=="projet")&(density_data["status"]=="Gagné"))]
density_data_cleaned = density_data_cleaned[~((density_data_cleaned["event"]=="passage_en_magasin")& (density_data_cleaned["timestamp_difference"]==timedelta(minutes=0)))]

density_data_cleaned.loc[density_data_cleaned.loc[:,"event"].apply(str.startswith,args=("crm",)),"event"]="crm"
density_data_cleaned.loc[density_data_cleaned.loc[:,"event"].apply(str.startswith,args=("iadvize",)),"event"]="iadvize"
density_data_cleaned.loc[density_data_cleaned.loc[:,"event"].apply(str.startswith,args=("demande",)),"event"]="demande"

density_data_cleaned.to_csv(cmd_folder+"data/processed/density_data_cleaned.csv",index=False)
