import pandas as pd
from find_dir import cmd_folder

## Important modifications of data resulting from exploration

buyer_history=pd.read_csv(cmd_folder+"data/interim/buyer_history_cleaned_crm.csv")

buyer_history = buyer_history.loc[list(buyer_history.loc[:,["buyer_id","timestamp","event"]].drop_duplicates().index),:]

mec_chelou = buyer_history.groupby("buyer_id")["event"].count().idxmax()
buyer_history = buyer_history[buyer_history["buyer_id"]!=mec_chelou].reset_index(drop=True)

buyer_history.to_csv(cmd_folder+"data/processed/buyer_history.csv",index=False)
