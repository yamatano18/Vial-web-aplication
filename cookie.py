from datetime import datetime
import datetime as dt
import sqlite3


def cookie_update(cookie, expires, login):
    expires = expires.strftime("%Y-%m-%d %H:%M:%S")
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET cookie = ?, expires = ? WHERE login = ?', (cookie, expires, login))
    conn.commit()


# def update_cookie(cookie, expires, login):
#    dbfile = '/home/wolonkia/vial/genbase.db'
#    conn = sqlite3.connect(dbfile)
#    cursor = conn.cursor()
#    expires = str(expires[0:19])
#    cursor.execute('UPDATE users SET cookie = ?, expires = ? WHERE login = ?;', (cookie, expires, login))
#    conn.commit()


# def check_cookie(cookie):
#    if cookie == '':
#        return ''
#   dbfile = '/home/wolonkia/vial/genbase.db'
#    conn = sqlite3.connect(dbfile)
#    cursor = conn.cursor()
#    cursor.execute('SELECT login, expires FROM users WHERE cookie = ?;', (cookie,))
#    data = cursor.fetchone()
#
#   if data is not None:
#       #time = dt.datetime.strptime(str(data[1]), "%Y-%m-%d %H:%M:%S")
#       time = str(data[1])[0:19]
#       if datetime.strptime(time, '%Y-%m-%d %H:%M:%S') > dt.datetime.now():
#            return str(data[0])
#    return ''


def cookie_check(cookie):
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('SELECT expires FROM users WHERE cookie = ?', (cookie,))
    expires = cursor.fetchone()

    if expires is not None:
        if dt.datetime.strptime(str(expires[0]), "%Y-%m-%d %H:%M:%S") > dt.datetime.now():
            return True
    return False


# def check_cookie(cookie):
#    if cookie == '':
#        return ''
#    dbfile = '/home/wolonkia/vial/genbase.db'
#    conn = sqlite3.connect(dbfile)
#    cursor = conn.cursor()
#    cursor.execute('SELECT login, expires FROM users WHERE cookie = ?', (cookie,))
#    data = cursor.fetchone()

#    if data is not None:
#        #time = dt.datetime.strptime(str(data[1]), "%Y-%m-%d %H:%M:%S")
#        time = str(data[1])[0:19]
#        if datetime.strptime(time, '%Y-%m-%d %H:%M:%S') > dt.datetime.now():
#            return str(data[0])
#    return ''

#def disable_cookie(cookie):
#    dbfile = '/home/wolonkia/vial/genbase.db'
#    conn = sqlite3.connect(dbfile)
#    cursor = conn.cursor()
#    expires = str(dt.datetime.utcnow())
#    cursor.execute('UPDATE users SET expires = ? WHERE cookie = ?;', (expires, cookie))
#    conn.commit()


def disable_cookie(cookie):
    expires = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dbfile = '/home/wolonkia/vial/genbase.db'
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET expires = ? WHERE cookie = ?', (expires, cookie))
    conn.commit()
