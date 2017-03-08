from find_dir import cmd_folder
import pandas as pd
import os
import json


buyer_history = pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")

sorted_history = buyer_history[["buyer_id","timestamp","event"]].sort_values(["buyer_id","timestamp","event"],ascending=True)

i=1
while i < len(sorted_history.index.values.tolist()):
    b = sorted_history.index.values.tolist()[i]
    a = sorted_history.index.values.tolist()[i-1]
    if((sorted_history["event"][b]== sorted_history["event"][a]) and (sorted_history["buyer_id"][b]==sorted_history["buyer_id"][a])):
        sorted_history["regroup"][b] = 1
    i+=1
    print(i)
  
regroup_history = sorted_history[["buyer_id","timestamp","event"]][sorted_history["regroup"]==0]