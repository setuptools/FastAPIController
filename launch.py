import os
from colorama import init 
import json
import subprocess

init()

with open("config.json","r+") as cfg_file:
    config = json.load(cfg_file)
cfg_file.close()

if config["bot_file"] != "":
    cwd = os.path.abspath(config["bot_file"])
    process = subprocess.Popen(["python" , str(cwd)], cwd = "\\".join(str(cwd).split("\\")[0:-1]) , creationflags= subprocess.CREATE_NEW_CONSOLE)

os.system(f"uvicorn server:app --host {config['fastapi']['host']} --port {config['fastapi']['port']} --reload")