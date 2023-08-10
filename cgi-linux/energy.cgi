#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cgi
from autogmx import autorun,mdrun,cd_energy

sys.stdout.write("Content-Type: text/plain\n\n")
mdrun()
autorun(cd_energy)
