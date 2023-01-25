import sqlite3

con = sqlite3.connect('project.sqlite')
cur = con.cursor()
with open('db.sql', 'r') as f:
    result = f.read()
cur.executescript(result)
cur.close()
con.close()
