# -*- coding: utf-8 -*-
from vial import render_template
import sqlite3
from redirect import redirect

def view(headers, body, data, snippet_title):
    snippet_title = str(snippet_title)
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('SELECT login FROM snippets WHERE title = ?;', (snippet_title,))
    login = cursor.fetchone()

    if login is None:
        return redirect(headers, body=body, data=data, message='Podany plik nie istnieje!'), 200, {}
    #snippet_path = 'od.iem.pw.edu.pl:2552/static/snippets/' + str(snippet_title) + '.snippet'
    snippet_title = str(snippet_title) + '.snippet'
    return render_template('html/view.html', body=body, data=data, headers=headers, snippet_title=snippet_title), 200, {}