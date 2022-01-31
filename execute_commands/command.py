#!/usr/bin/env python3

import subprocess  # https://docs.python.org/3/library/subprocess.html

command = "pstree"

subprocess.Popen(command, shell=True)
