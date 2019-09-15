#!/usr/bin/python3

"""Create user database and common user management utilities"""

#import os, sys
from hashlib import sha256
import sqlite3, os
import uuid, pyotp


def password_gen(length=8):
    import string, secrets
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def reset_database(db_path):
    """Assert that the sqlite database exist and empty"""
    if os.path.isfile(db_path):
        os.unlink(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Create table
    try:
        cur.execute('''CREATE TABLE user (id  INTEGER PRIMARY KEY, username text UNIQUE, email text, auth_type text, password_hash text, otp_password text, otp_enabled integer)''')
        return conn
    except Exception as e:
        print(e)
        return None


def get_user(conn, username):
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return cur.execute("SELECT * FROM user WHERE username = '{username}'".format(username=username)).fetchone()


def create_user(conn, username, email, auth_type='local', password=None, otp_password=None, otp_enabled=1):
    cur = conn.cursor()
    if not password:
        password = password_gen(length=6)
    if not otp_password:
        otp_password = pyotp.random_base32()

    try:
        cur.execute("""REPLACE INTO user(username, email, auth_type, password_hash, otp_password, otp_enabled)
            VALUES('{username}', '{email}', '{auth_type}', '{password_hash}', '{otp_password}', '{otp_enabled}')""".format(
                    username=username,
                    email=email,
                    auth_type=auth_type,
                    password_hash=hash_password(password),
                    otp_password=otp_password,
                    otp_enabled=otp_enabled
                )
            )
        cur.close()
        conn.commit()
        return (password, otp_password)
    except Exception as e:
        print(e)
        return ()


def delete_user(conn, username):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM user WHERE username = '{username}'".format(username=username) )
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(e)
        return False


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == sha256(salt.encode() + user_password.encode()).hexdigest()


def authenticate(conn, username, passphrase):
    user = get_user(conn, username)
    if user:
        if user['auth_type'] == 'local':
            if user['otp_enabled'] == 1:
                import pyotp
                otp_input = passphrase[-6:]
                password_input = passphrase[0:-6]
                if check_password(user['password_hash'], password_input):
                    totp = pyotp.TOTP(user['otp_password'])
                    return totp.now() == otp_input
            else:
                return check_password(user['password_hash'], passphrase)

    return False


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # import code
    # code.interact(local=locals())
    import IPython
    IPython.embed()