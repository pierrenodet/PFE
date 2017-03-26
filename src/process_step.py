import pandas as pd
from find_dir import cmd_folder

non_buyer_history=pd.read_csv(cmd_folder + "data/interim/non_buyer_history.csv")
