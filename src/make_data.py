import os
from find_dir import cmd_folder

#Here will be put the script needed to download data from a future database or script to get data from other sources
#for the moment the data are put by hand in PFE/data/raw/
os.makedirs(cmd_folder+"data/raw/", exist_ok=True)
print("Mettez les export_ensai_buyersHistory_170216.csv et export_ensai_buyersProfil_170216.csv dans PFE/data/raw/")
