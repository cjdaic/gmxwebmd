#!/usr/bin/python3
# -*- coding: utf-8 -*-
# nph-script

import sys
import cgi
import os
from autogmx import autorun,cd_grep
sys.stdout.write("Content-Type: text/plain\n\n")

os.chdir("/var/www/html/usr")
autorun(cd_grep)
