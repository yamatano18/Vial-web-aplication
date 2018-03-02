# -*- coding: utf-8 -*-
import uuid
from vial import render_template
import datetime as dt
from redirect import redirect
import sqlite3
from cookie import cookie_check


def addsnippet(headers, body, data):
    #login = str(data['login']) if 'login' in data else ''
    # password = str(data['password']) if 'password' in data else ''
    cookie = str(headers['http-cookie']).replace('sessionid=', '')
    if not cookie_check(cookie):
        return redirect(headers=headers, body=body, data=data, message="Nieautoryzowana proba dodania snippet'a!")

    snippet_content = str(data['snippet']) if 'snippet' in data else ''
    title = str(data['title']) if 'title' in data else ''

    if (title == '' or snippet_content == ''):
        return render_template('html/addsnippet.html', body=body, data=data, headers=headers, cookie=cookie), 200, {}
    elif len(title) > 60:
        return render_template('html/addsnippet.html', body=body, data=data, headers=headers, cookie=cookie,
                               message="Maksymalna dlugosc nazwy snippet'a to 24 znaki!"), 200, {}
    elif len(snippet_content) > 9999:
        return render_template('html/addsnippet.html', body=body, data=data, headers=headers, cookie=cookie,
                               message="Dodany przez Ciebie plik jest zbyt dlugi!"), 200, {}

    add_snippet(title, snippet_content, cookie)
    return redirect(headers=headers, body=body, data=data, message='Snippet zostal dodany!')


def add_snippet(title, snippet_content, cookie):
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('SELECT login FROM users WHERE cookie = ?;', (cookie,))
    login = str(cursor.fetchone()[0])
    cursor.execute('SELECT time FROM snippets ORDER BY time;')
    date_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO snippets VALUES (?, ?, ?);', (title, login, date_time))
    conn.commit()
    snippet_path = 'static/snippets/' + title + '.snippet'
    snippet_file = open(snippet_path, 'w+')
    snippet_file.write(snippet_content)
    snippet_file.close()
