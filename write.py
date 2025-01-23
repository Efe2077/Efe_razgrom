import sqlite3


def check_admin(name, email):
    con = sqlite3.connect('db/admins.db')
    cur = con.cursor()
    res = cur.execute(f"""SELECT name, email FROM Admins WHERE (email = '{email}' AND name = '{name}')""").fetchall()
    if res:
        return True
    else:
        return False
