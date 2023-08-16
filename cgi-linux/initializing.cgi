#!/usr/bin/python3

import sys
import os
import subprocess
#from time import sleep
import shlex
import cgi
sys.stdout.write("Content-Type: text/plain\n\n")
#print("Content-Type: text/plain; charset=utf-8\n")
#print('')
sys.stdout.flush()

os.chdir("/var/www/html/")
subprocess.run('ls', shell=True)
subprocess.run('rm -r /var/www/html/usr', shell=True)
subprocess.run('cp -r /var/www/html/usr-backup /var/www/html/usr', shell=True)
subprocess.run('ls', shell=True)