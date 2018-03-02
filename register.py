from vial import render_template
import datetime as dt
import uuid
import math
import string
import random
from random import choice
import hashlib
import sqlite3
from redirect import redirect


def register(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    repassword = str(data['repassword']) if 'repassword' in data else ''
    # dbfile = '/home/wolonkia/vial/genbase.db'
    if (login == '') and (password == '') and (repassword == ''):
        return render_template('html/register.html', body=body, data=data, headers=headers), 200, {}
    elif not login_length(login):
        return render_template('html/register.html', body=body, data=data, headers=headers,
                               message='Wymagana dlugosc loginu od 4 do 16. znakow!'), 200, {}
    elif not login_chars(login):
        return render_template('html/register.html', body=body, data=data, headers=headers,
                               message='Login zawiera niepoprawne znaki!'), 200, {}
    elif not login_exists(login):
        return render_template('html/register.html', body=body, data=data, headers=headers,
                               message='Login juz zajety!'), 200, {}
    elif not password_length(password):
        return render_template('html/register.html', body=body, data=data, headers=headers,
                               message='Wymagana dlugosc hasla od 4 do 24 znakow!'), 200, {}
    elif not same_passwords(password, repassword):
        return render_template('html/register.html', body=body, data=data, headers=headers,
                               message='Podane hasla nie sa identyczne!'), 200, {}
    elif entropy(password) < 45.0:
        return render_template('html/register.html', body=body, data=data, headers=headers,
                               message='Haslo jest zbyt slabe, jego entropia: ' + str(
                                   round(entropy(password), 2))), 200, {}
    cookie = str(uuid.UUID(bytes=random_bytes(16)).hex)
    expires = (dt.datetime.utcnow() + dt.timedelta(minutes=20))
    add_user(login, password, cookie, expires.strftime("%Y-%m-%d %H:%M:%S"))
    # expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
    # cookie = 'sessionid=' + cookie + '; expires=' + expires  # + " ; secure"
    return render_template('html/redirect.html', body=body, data=data, headers=headers,
                           message='Rejestracja zakonczona pomyslnie!'), 200, {}


def add_user(login, password, cookie, expires):
    salt = ''.join(random.sample(string.ascii_letters, 20))
    for i in range(3):
        password = salt.join(password)
        password = str(hashlib.sha1(password).hexdigest())
    password = salt + password
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    expires = expires[0:19]
    cur.execute('INSERT INTO "users" VALUES (?, ?, ?, ?);', (login, password, cookie, expires))
    conn.commit()
    conn.close()


def password_length(password):
    if 4 <= len(password) <= 24:
        return True
    return False


def same_passwords(password, repassword):
    if str(password) == str(repassword):
        return True
    return False


def login_chars(login):
    for c in login:
        if not (96 < ord(c) < 123) or (64 < ord(c) < 91) or (47 < ord(c) < 58):
            return False
    return True


def login_length(login):
    if 4 <= len(login) <= 24:
        return True
    return False


def login_exists(login):
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute("SELECT login FROM users WHERE login = ?;", (login,))

    if cur.fetchone() is None:
        return True
    return False


def entropy(password):
    small = big = num = spec = 0
    for c in password:
        if 96 < ord(c) < 123:
            small += 1
        elif 64 < ord(c) < 91:
            big += 1
        elif 47 < ord(c) < 58:
            num += 1
        else:
            spec += 1
    alpha = small * 26 + big * 26 + num * 10 + spec * 66
    entropy = len(password) * math.log(alpha if alpha > 0 else 1, 2)
    return entropy


def random_bytes(n):
    allbytes = [chr(i) for i in range(256)]
    bytes = []
    for _ in range(n):
        bytes.append(choice(allbytes))
    return str(''.join(bytes))
