#!C:\Users\CJ\AppData\Local\Programs\Python\Python39\python.exe
# -*- coding: utf-8 -*-

import sys
import os
import configparser
from io import StringIO
import json
import cgi

os.chdir("D:/apache/Apache24/htdocs/usr")
sys.stdout.write("Content-Type: text/plain\n\n")
sys.stdout.flush()
def read_mdp_file(file_path):
    with open(file_path, 'r') as f:
        content = '[root]\n' + f.read()  # Add a root section to make it a valid INI file
    config = configparser.ConfigParser(allow_no_value=True, strict=False, comment_prefixes=(";",))
    config.read_string(content)
    return config

def write_mdp_file(config, file_path):
    content = StringIO()
    config.write(content)
    with open(file_path, 'w') as f:
        f.write(content.getvalue().replace('[root]\n', ''))

def change_nsteps_in_mdp_file(file_path, new_value):
    config = read_mdp_file(file_path)
    config.set('root', 'nsteps', str(new_value))
    write_mdp_file(config, file_path)

def change_nsteps_in_directory(directory_path, new_value):
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.mdp'):
            file_path = os.path.join(directory_path, file_name)
            change_nsteps_in_mdp_file(file_path, new_value)

with open("usr.json","r",encoding='utf-8') as usr_conf:
    f = usr_conf.read()
    usr_data = json.loads(f)
directory_path = 'D:/apache/Apache24/htdocs/usr'
new_nsteps_value = usr_data.get("nstep")
change_nsteps_in_directory(directory_path, new_nsteps_value)