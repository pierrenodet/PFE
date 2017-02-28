from find_dir import cmd_folder
import os

## Importing Data

buyer_history = pd.read_csv(cmd_folder+"data/processed/buyer_history.csv")

sorted_history = buyer_history[["buyer_id","timestamp","event","status"]].sort_values(["buyer_id","timestamp"],ascending=True)

with open(cmd_folder+"data/processed/trace.json","w") as buf:
    buf.write("[")
    buyers = sorted_history["buyer_id"].unique()
    for buyer in buyers[0:buyers.size-1]:
        buf.write("{\"id\":\""+buyer+"\",\"trace\":")
        sorted_history[sorted_history["buyer_id"]==buyer][["event","status"]].to_json(path_or_buf=buf,orient="records",force_ascii=False)
        buf.write("},\n")
    buf.write("{\"id\":\""+buyer+"\",\"trace\":")
    sorted_history[sorted_history["buyer_id"]==buyer][["event","status"]].to_json(path_or_buf=buf,orient="records",force_ascii=False)
    buf.write("}]")

trace = json.load(open(cmd_folder+"data/processed/trace.json","r"))
