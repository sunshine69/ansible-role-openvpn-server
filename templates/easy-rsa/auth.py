#!/usr/bin/python3

from user_mngt import authenticate

import os, sys, sqlite3

os.chdir(os.path.dirname(os.path.realpath(__file__)))

username = os.getenv("username")
password = os.getenv("password")

conn = sqlite3.connect('user.db')

if authenticate(conn, username, password):
    sys.exit(0)
else:
    sys.exit(1)    