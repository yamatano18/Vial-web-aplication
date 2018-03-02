import sqlite3
dbfile = '/home/wolonkia/vial/genbase.db'
def index(req, key=''):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    html = '<html>'
    html += 'Key: %s <br/>' % key
        query = "SELECT * FROM users"
    for row in c.execute(query):
        html += '%s <br/>' % row[1]
    html += '</html>'
    return html
