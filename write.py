import sqlite3


def check_admin(name):
    con = sqlite3.connect('db/admins.db')
    cur = con.cursor()
    res = cur.execute(f"""SELECT name FROM Admins WHERE name = '{name}'""").fetchall()
    if res:
        return True
    else:
        return False
