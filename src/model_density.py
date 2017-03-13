import pandas as pd
from datetime import timedelta
from find_dir import cmd_folder
from clean_data import stringlist_to_datelist

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

#density_data_cleaned = density_data[~((density_data["event"]=="projet")&(density_data["status"]=="Gagné"))]
#density_data_cleaned = density_data_cleaned[~((density_data_cleaned["event"]=="passage_en_magasin")& (density_data_cleaned["timestamp_difference"]==timedelta(minutes=0)))]

first_event_timestamp = density_percentage[["buyer_id","timestamp"]].groupby("buyer_id").min().reset_index()
density_percentage = pd.merge(density_percentage,first_event_timestamp,on="buyer_id")
density_percentage.rename(columns={'timestamp_x':'timestamp','timestamp_y':'first_event_timestamp'},inplace=True)

density_percentage["timestamp_percentage"]=(density_percentage["timestamp"]-density_percentage["first_event_timestamp"])/(density_percentage["last_purchase_timestamp"]-density_percentage["first_event_timestamp"])

density_percentage.drop(density_percentage[density_percentage["event"]=="quote_lose"].index.values,inplace=True)

density_percentage.to_csv(cmd_folder+"data/processed/density_percentage.csv",index=False)
