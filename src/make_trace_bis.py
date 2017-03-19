from find_dir import cmd_folder
import pandas as pd
import os
import json
import numpy as np


buyer_history = pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")

sorted_history = buyer_history[["buyer_id","visit_id","timestamp","event"]].sort_values(["buyer_id","visit_id","timestamp","event"],ascending=True)

sorted_history["regroup"] = False

##Version Beaucoup trop Longue
#a = sorted_history.index.values.tolist()[0]
#visit_en_cours = sorted_history["visit_id"][a]
#pageview_deja_present = False
#chat_deja_present = False
#
#for i in range(len(sorted_history.index.values.tolist())-1):   
#    print(i)
#    b = sorted_history.index.values.tolist()[i+1]
#    if(sorted_history["visit_id"][b] == visit_en_cours):
#        if(sorted_history["event"][b]=="pageview"):
#            if(pageview_deja_present):
#                sorted_history["regroup"][b] = 1
#            else:
#                pageview_deja_present = True
#        else: 
#            if (sorted_history["event"][b]=="chat"):
#                if(chat_deja_present):
#                    sorted_history["regroup"][b] = 1
#                else:
#                    chat_deja_present = True
#    else :
#         visit_en_cours=sorted_history["visit_id"][b]
#         pageview_deja_present= False
#         chat_deja_present=False
#           
#          
#
#sorted_history["regroup2"]=(sorted_history["regroup"]==1)
#
#
#regroup_history = sorted_history[["buyer_id","timestamp","event"]][sorted_history["regroup2"]==False]
#

## Autre version

total_pageview_chat = sorted_history["visit_id"][sorted_history["event"]=="pageview"].index.values.tolist()
total_pageview_chat.extend(sorted_history["visit_id"][sorted_history["event"]=="chat"].index.values.tolist())


unique = sorted_history["visit_id"][sorted_history["event"]=="pageview"].drop_duplicates().index.values.tolist()
unique.extend( sorted_history["visit_id"][sorted_history["event"]=="chat"].drop_duplicates().index.values.tolist())

duplicate_pageview_chat = list((set(total_pageview_chat) - set(unique)))
index_without_duplicates = list(set(sorted_history.index.values.tolist()) - set(duplicate_pageview_chat))

regroup_history= sorted_history[["buyer_id","timestamp","event"]].loc[index_without_duplicates]

#for i in range(len(sorted_history.index.values.tolist())):
#    b = sorted_history.index.values.tolist()[i]
#    if((sorted_history["event"][b]=="pageview") or (sorted_history["event"][b]=="chat")):
#        if(not(b in unique)):
#            sorted_history["regroup"][b] = True
#    print(i)
#    
#
#regroup_history = sorted_history[["buyer_id","timestamp","event"]][sorted_history["regroup"]==False]

    
### Nouvelle Version
#index = sorted_history.index.values.tolist()
#index_decal = index[0:len(index)-1]
#index_decal.insert(0,0)
#
#cond1 = np.array((sorted_history["event"][index]==sorted_history["event"][index_decal]).tolist())
#cond2 =  np.array((sorted_history["buyer_id"][index]==sorted_history["buyer_id"][index_decal]).tolist())
#sorted_history["regroup"] = (cond1 & cond2).tolist()
#
#
#regroup_history = sorted_history[["buyer_id","timestamp","event"]][sorted_history["regroup"]==False]
#

with open(cmd_folder+"data/processed/trace_regroup.json","w") as buf:
    buf.write("[")
    buyers = regroup_history["buyer_id"].unique()
    for buyer in buyers[0:buyers.size-1]:
        buf.write("{\"id\":\""+buyer+"\",\"trace\":")
        regroup_history[regroup_history["buyer_id"]==buyer][["event"]].to_json(path_or_buf=buf,orient="records",force_ascii=False)
        buf.write("},\n")
    buf.write("{\"id\":\""+buyer+"\",\"trace\":")
    regroup_history[regroup_history["buyer_id"]==buyer][["event"]].to_json(path_or_buf=buf,orient="records",force_ascii=False)
    buf.write("}]")

trace = json.load(open(cmd_folder+"data/processed/trace_regroup.json","r"))
