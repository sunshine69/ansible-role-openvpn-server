#!/usr/bin/python3

import json
import os
import sqlite3
from user_mngt import reset_database, create_user, get_user
import argparse

import pyotp
import qrcode

os.chdir(os.path.dirname(os.path.realpath(__file__)))

parser = argparse.ArgumentParser()
parser.add_argument("-u", help="username", required=True)
parser.add_argument("-email", help="user email address", required=True)
parser.add_argument("-auth_type", help="Authentication type - string - can be 'local'", required=False, default='local')
parser.add_argument("-p", help="password - auto generated", required=False, default=None)
parser.add_argument("-otp",help="otp password - auto generated", required=False, default=None)
parser.add_argument("-otp_enabled", help="otp_enabled - 0/1", required=False, default=1, type=int)
parser.add_argument("-db_file", help="database file path", required=False, default='user.db')
parser.add_argument("-reset_db", help="Reset the database", required=False, default='no')
parser.add_argument("-U", help="Update existing user", required=False, default='no')

args, conn = parser.parse_args(), None

db_file = args.db_file

if not os.path.exists(db_file) or args.reset_db == 'yes':
    conn = reset_database(db_file)
else:
    conn = sqlite3.connect(db_file)

existing_user = get_user(conn, args.u)

if (not existing_user) or args.U == 'yes':
    password, otp_password = create_user(conn, args.u, email=args.email, auth_type=args.auth_type, \
        password=args.p, otp_password=args.otp, otp_enabled=args.otp_enabled)

    import socket
    hostname = socket.gethostname()
    uri = pyotp.TOTP(otp_password).provisioning_uri("%s@vpn-%s" % (args.u, hostname[-12:]))

    import qrcode

    img = qrcode.make(uri)
    img.save("generated/%s-qr.png" % args.u)
    os.system("chmod 0600 generated/%s-qr.png" % args.u)

    print(json.dumps({'username': args.u, 'password': password, 'state': 'updated', 'email': args.email}, indent=4, sort_keys=True))

else:
    print(json.dumps({'username': args.u, 'password': 'N/A', 'state': 'existed', 'email': existing_user['email']}, indent=4, sort_keys=True))