from vial import Vial, render_template
from redirect import redirect
from cookie import cookie_check, cookie_update
from datetime import datetime
from register import random_bytes
import datetime as dt
import hashlib
import sqlite3
import uuid


def signin(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    cookie = str(headers['http-cookie']).replace('sessionid=', '')

    if (login == '') and (password == ''):
        if cookie_check(cookie):
            return render_template('html/home.html', body=body, data=data, headers=headers,
                                   message='Jestes juz zalogowany!'), 200, {}
        return render_template('html/signin.html', body=body, data=data, headers=headers), 200, {}

    # login = str(data['login']) if 'login' in data else ''
    # password = str(data['password']) if 'password' in data else ''
    # dbfile = '/home/wolonkia/vial/genbase.db'
    # conn = sqlite3.connect(dbfile)
    # cursor = conn.cursor()

    # dbpassword = cursor.execute('SELECT password FROM users WHERE login = ?', (login,))
    # passwd = ''
    # for row in dbpassword:
    #    passwd = str(row[0])

    # salt = passwd[:20]
    # for i in range(3):
    #    password = salt.join(password)
    #    password = str((hashlib.sha1(password)).hexdigest())
    # password = salt + password

    # if (login == '') or (password == ''):
    #    cookie = str(headers['http-cookie']).replace('session_id=', '')
    #    if cookie_check(cookie):
    #        return redirect(headers=headers, body=body, data=data, message='Jestes juz zalogowany!')

    #    return render_template('html/signin.html', body=body, data=data, headers=headers), 200, {}

    elif allow_signin(login, headers):
        if authentication(login, password):
            cookie = str(uuid.UUID(bytes=random_bytes(16)).hex)
            expires = dt.datetime.now() + dt.timedelta(minutes=20)
            cookie_update(cookie, expires, login)
            expires = (dt.datetime.utcnow() + dt.timedelta(minutes=20)).strftime("%a, %d %b %Y %H:%M:%S GMT")
            cookie = 'sessionid=' + cookie + '; expires=' + expires + ";" + "secure"
            add_log(headers, data, True)
            return render_template('html/home.html', body=body, data=data, headers=headers,
                                   message='Zostales zalogowany!'), 200, {'Set-Cookie': cookie}
        add_log(headers, data, False)
        return render_template('html/signin.html', body=body, data=data, headers=headers,
                               message='Nieprawidlowe dane logowania!'), 200, {}
    add_log(headers, data, False)
    return render_template('html/signin.html', body=body, data=data, headers=headers,
                           message='Zbyt wiele blednych prob zalogowania!'), 200, {}

    # elif (password == passwd):
    # return render_template('html/signin.html', body=body, data=data, headers=headers,
    #                       message='Zostales zalogowany!'), 200, {'Set_cookie': cookie}
    # return render_template('html/signin.html', body=body, data=data, headers=headers,
    #                  message='Podales nieprawidlowe dane!'), 200, {}


def allow_signin(login, headers):
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT is_connected, date_time FROM logs WHERE login = ? AND ip = ? ORDER BY date_time DESC LIMIT 3;',
        (login, ip))
    cursor_length = 0
    last_login = ''
    for result in cursor.fetchall():
        cursor_length += 1
        if str(result[0]) == '1':
            return True
        if cursor_length == 1:
            last_login = str(result[1])
    if cursor_length < 10:
        return True

    allow_after = datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S') + dt.timedelta(minutes=10)
    if dt.datetime.now() > allow_after:
        return True
    return False


def add_log(headers, data, success=False):
    login = str(data['login']) if 'login' in data else '-'
    ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    if success:
        cursor.execute('INSERT INTO logs VALUES (?, ?, ?, "TRUE");', (login, ip, date_time))
    else:
        cursor.execute('INSERT INTO logs VALUES (?, ?, ?, "FALSE");', (login, ip, date_time))
    conn.commit()


def authentication(login, password):
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE login = ?;', (login,))
    dbhash = cursor.fetchone()
    dbhash = str(dbhash[0])
    salt = dbhash[0:20]
    for i in range(3):
        password = salt.join(password)
        password = str(hashlib.sha1(password).hexdigest())
    hash = salt + password
    if hash == dbhash:
        return True
    return False
