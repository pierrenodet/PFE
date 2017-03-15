import os
from find_dir import cmd_folder
import paramiko
import yaml
import pandas as pd

with open(cmd_folder+"config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

#Here will be put the script needed to download data from a future database or script to get data from other sources
#for the moment the data are put by hand in PFE/data/raw/
os.makedirs(cmd_folder+"data/raw/", exist_ok=True)
os.makedirs(cmd_folder+"data/interim/", exist_ok=True)
os.makedirs(cmd_folder+"data/processed/", exist_ok=True)

print("Mettez les export_ensai_buyersHistory_170216.csv et export_ensai_buyersProfil_170216.csv et PFEensai2017_description_des_donnees.xlsx dans PFE/data/raw/")

transport = paramiko.Transport((cfg["host"],cfg["port"]))
transport.connect(username = cfg["user"],password = cfg["pwd"])
sftp = paramiko.SFTPClient.from_transport(transport)
if ~os.path.isfile(cmd_folder+"data/raw/export_ensai_history_170307170002.csv"):
    sftp.get("/export_ensai_history_170307170002.csv",cmd_folder+"data/raw/export_ensai_history_170307170002.csv")
#if ~os.path.isfile(cmd_folder+"data/raw/export_ensai_history_170307170002.headers")
#    sftp.get("/export_ensai_history_170307170002.headers",cmd_folder+"data/raw/export_ensai_history_170307170002.headers")
if ~os.path.isfile(cmd_folder+"data/raw/export_ensai_user_170307170002.csv"):
    sftp.get("/export_ensai_user_170307170002.csv",cmd_folder+"data/raw/export_ensai_user_170307170002.csv")
#if ~os.path.isfile(cmd_folder+"data/raw/export_ensai_user_170307170002.headers")
#    sftp.get("/export_ensai_user_170307170002.headers",cmd_folder+"data/raw/export_ensai_user_170307170002.headers")

os.makedirs(cmd_folder+"output/picture/", exist_ok=True)
os.makedirs(cmd_folder+"output/data/", exist_ok=True)
#ensai_2017 FTP
