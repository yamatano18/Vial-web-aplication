from vial import render_template
import sqlite3
from cookie import cookie_check


def home(headers, body, data):
    login = str(data['login']) if 'login' in data else ''
    password = str(data['password']) if 'password' in data else ''
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    # if (login == '') and (password == ''):
    if cookie_check(cookie):
        dbfile = '/home/wolonkia/vial/genbase.db'
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        cursor.execute('SELECT title, login, time FROM snippets ORDER BY time')
        snippets_result = cursor.fetchall()
        snippets_values = []
        for row in snippets_result:
            snippets_values.append({'title': str(row[0]), 'login': str(row[1]), 'date': str(row[2])})
        cursor.execute('SELECT login FROM users WHERE cookie = ?;', (cookie,))
        login = str(cursor.fetchone()[0])
        print login
        cursor.execute('SELECT ip FROM logs WHERE login = ? ORDER BY date_time DESC', (login,))
        fetch = cursor.fetchall()
        if len(fetch) >= 2:
            if str(fetch[0][0]) != str(fetch[1][0]):
                return render_template('html/home.html', body=body, data=data, headers=headers,
                                       snippets_values=snippets_values,
                                       message='Wykryto nowe polaczenie do Twojego konta z ip: ' + str(
                                           fetch[1][0])), 200, {}
        return render_template('html/home.html', body=body, data=data, headers=headers,
                               snippets_values=snippets_values,
                               message="Witaj '" + login + "'"), 200, {}

    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('SELECT title, login, time FROM snippets ORDER BY time')
    snippets_result = cursor.fetchall()
    snippets_values = []
    for row in snippets_result:
        snippets_values.append({'title': str(row[0]), 'login': str(row[1]), 'date': str(row[2])})
    return render_template('html/home.html', body=body, data=data, headers=headers, snippets_values=snippets_values,
                           message='Witaj na stronie!'), 200, {'Set-Cookie': cookie}
