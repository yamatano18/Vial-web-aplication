from vial import Vial, render_template
from redirect import redirect
from cookie import cookie_check
import hashlib
import sqlite3
import string
import random
from register import password_length, same_passwords, entropy


def editpassword(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    oldpassword = str(data['oldpassword']) if 'oldpassword' in data else ''
    password = str(data['password']) if 'password' in data else ''
    repassword = str(data['repassword']) if 'repassword' in data else ''
    if (login == '') and (password == ''):
        cookie = str(headers['http-cookie']).replace('sessionid=', '')
        if not cookie_check(cookie):
            return render_template('html/signin.html', body=body, data=data, headers=headers,
                                   message='Musisz sie zalogowac aby zmienic haslo!'), 200, {}
        dbfile = '/home/wolonkia/vial/genbase.db'
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('SELECT login FROM users WHERE cookie = ?;', (cookie,))
        login = str(cursor.fetchone()[0])
        cursor.execute('SELECT password FROM users WHERE login = ?;', (login,))
        oldpassword = str(cursor.fetchone()[0])

        if oldpassword == password:
            update_password(login, password)
            # expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
            # cookie = 'sessionid=' + cookie + '; expires=' + expires  # + " ; secure"
            return render_template('html/home.html', body=body, data=data, headers=headers,
                                   message='Haslo zostalo zmienione pomyslnie!'), 200, {}
    if (oldpassword == '') or (repassword == ''):
        return render_template('html/editpassword.html', body=body, data=data, headers=headers), 200, {}
        if password_length(password):
            return render_template('html/editpassword.html', body=body, data=data, headers=headers,
                                   message='Wymagana dlugosc hasla od 4 do 24 znakow!'), 200, {}
        if not same_passwords(password, repassword):
            return render_template('html/editpassword.html', body=body, data=data, headers=headers,
                                   message='Podane hasla nie sa identyczne!'), 200, {}
        if entropy(password) < 45.0:
            return render_template('html/editpassword.html', body=body, data=data, headers=headers,
                                   message='Haslo jest zbyt slabe, jego entropia: ' + str(
                                       round(entropy(password), 2))), 200, {}
        return render_template('html/home.html', body=body, data=data, headers=headers), 200, {}

        # return render_template('html/editpassword.html', body=body, data=data, headers=headers), 200, {}
    return render_template('html/home.html', body=body, data=data, headers=headers,
                           message='Witaj na stronie!'), 200, {}


def update_password(login, password):
    salt = ''.join(random.sample(string.ascii_letters, 20))
    for i in range(3):
        password = salt.join(password)
        password = str(hashlib.sha1(password).hexdigest())
    password = salt + password
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute('UPDATE users SET password = ? WHERE login = ?;', (password, login))
    conn.commit()
    conn.close()
