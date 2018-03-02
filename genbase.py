from sqlite3 import *
db = connect('genbase.db')
cur = db.cursor()
cur.execute('CREATE TABLE users(login VARCHAR(16), password VARCHAR(60), cookie VARCHAR(32), expires DATETIME)')
#cur.execute("INSERT INTO users VALUES('admin', 'EJIKlBcTXHMspbPkgtQL9e9a747c56aa841401dc8046d5a038ed52f76000', '4c34ec09538a3755e6e4539553805417', '2017-06-12 17:00:00')")
#cur.execute("INSERT INTO users VALUES('user', 'WjuqMXOVwbGZfcSzdYlt37973776b6b2eeae4215c1441a1d315b12895978', '537524360d6be0dee0c3572fe32da17c', '2017-06-12 17:00:00')")

cur.execute('CREATE TABLE logs(login VARCHAR(16), ip VARCHAR(15), date_time DATETIME, is_connected BOOLEAN)')

cur.execute('CREATE TABLE snippets(title VARCHAR(24), login VARCHAR(16), time DATETIME)')

db.close()
