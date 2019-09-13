#!/usr/bin/python3

import os, sys
import pam

p = pam.pam()
username = os.getenv("username")
password = os.getenv("password")

if p.authenticate(username, password):
    print("Auth SUCCESS")
    sys.exit(0)
else:
    print("Auth FAIL")
    sys.exit(1)