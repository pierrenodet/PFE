##Importing Config File

import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

data_dir = cfg['paths']['data_dir']

##Importing Data

import pandas as pd

history=pd.read_csv(data_dir + "export_ensai_buyersHistory_170216.csv",sep="\t",header=None)
history.columns=["buyer_id","visit_id","timestamp","event","status"]

#Regardons 
history.groupby("buyer_id")["event"].count().describe()
