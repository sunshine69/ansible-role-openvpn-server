#!/usr/bin/python3

import os, sys
import json
import re

input_file = sys.argv[1]

data = open(input_file, 'r').readlines()

empty_or_commented_line_ptn = re.compile(r'(^[\s]*#.*|^[\s]*[\n]{0,1}$)')
parse_email_pnt = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
parse_username_ptn = re.compile(r"^([^\s\@]+)\s")
parse_state_ptn = re.compile(r'\bstate=(remove|delete|absent)\b')
parse_otp_ptn = re.compile(r'\botp_enabled=(no|0|disabled)\b')
parse_reset_ptn = re.compile(r'\breset\b')
parse_password_length_ptn = re.compile(r'\bpassword_length=([\d]+)\b')

output = []

for line in data:
    if empty_or_commented_line_ptn.search(line):
        continue
    m = parse_email_pnt.search(line)
    if m:
        email = m.group(1)
        email = email.lower()
    else:
        continue
    m = parse_username_ptn.search(line)
    if m:
        username = m.group(1)
    else: # Create user name from email
        username, _domain = email.split('@')
        username = username.lower()
    reset = 'yes' if parse_reset_ptn.search(line) else 'no'
    state = 'absent' if parse_state_ptn.search(line) else 'present'
    otp_enabled = 0 if parse_otp_ptn.search(line) else 1
    m = parse_password_length_ptn.search(line)
    password_length = m.group(1) if m else 6

    output.append({
            'username': username,
            'email': email,
            'reset': reset,
            'otp_enabled': otp_enabled,
            'password_length': password_length,
            'state': state
        })

print(json.dumps(output))
