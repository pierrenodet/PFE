import pandas as pd
from find_dir import cmd_folder
from clean_data import stringlist_to_datelist
from datetime import timedelta

## Important modifications of data resulting from exploration

buyer_history=pd.read_csv(cmd_folder+"data/interim/buyer_history.csv")

buyer_history = buyer_history.loc[list(buyer_history.loc[:,["buyer_id","timestamp","event"]].drop_duplicates().index),:]

buyer_history.drop(pd.merge(buyer_history, pd.DataFrame(buyer_history.groupby("buyer_id")["event"].count().sort_values(ascending=False)[0:4].index), on=["buyer_id"],right_index=True).index,inplace=True)

buyer_history["timestamp"]=stringlist_to_datelist(buyer_history["timestamp"])

diff_ts = (buyer_history.groupby("buyer_id")["timestamp"].max()-buyer_history.groupby("buyer_id")["timestamp"].min()).apply(timedelta.total_seconds)
buyer_history = pd.merge(buyer_history,pd.DataFrame(diff_ts[diff_ts>86400].index),on="buyer_id",how="inner")

len_trace = buyer_history.groupby("buyer_id").size()
buyer_history = pd.merge(buyer_history,pd.DataFrame(len_trace[len_trace>3].index),on="buyer_id",how="inner")

buyer_history.to_csv(cmd_folder+"data/processed/buyer_history.csv",index=False)
