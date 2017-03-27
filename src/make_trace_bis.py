from find_dir import cmd_folder
import pandas as pd
import os
import json
import numpy as np

buyer_history = pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")

sorted_history = buyer_history[["buyer_id","visit_id","timestamp","event"]].sort_values(["buyer_id","visit_id","timestamp","event"],ascending=True)

sorted_history["regroup"] = False

total_pageview_chat = sorted_history["visit_id"][sorted_history["event"]=="pageview"].index.values.tolist()
total_pageview_chat.extend(sorted_history["visit_id"][sorted_history["event"]=="chat"].index.values.tolist())

unique = sorted_history["visit_id"][sorted_history["event"]=="pageview"].drop_duplicates().index.values.tolist()
unique.extend( sorted_history["visit_id"][sorted_history["event"]=="chat"].drop_duplicates().index.values.tolist())

duplicate_pageview_chat = list((set(total_pageview_chat) - set(unique)))
index_without_duplicates = list(set(sorted_history.index.values.tolist()) - set(duplicate_pageview_chat))

regroup_history= sorted_history[["buyer_id","timestamp","event"]].loc[index_without_duplicates]

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
