#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cgi
from autogmx import autorun,cd_pdb2gmx,usr_data,ignh
sys.stdout.write("Content-Type: text/plain\n\n")

autorun(cd_pdb2gmx)
