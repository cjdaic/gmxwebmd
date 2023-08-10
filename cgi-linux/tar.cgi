#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tarfile
import cgi
import os
import sys
sys.stdout.write("Content-Type: text/plain\n\n")
os.chdir("/var/www/html")
folder_to_tar = "usr"
tar_file_path = "usr/user.tar"

with tarfile.open(tar_file_path, "w") as tar_file:
    tar_file.add(folder_to_tar)
    tar_file.close()

sys.stdout.write("File tarred\n")