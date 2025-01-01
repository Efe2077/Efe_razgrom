import sqlite3


def check_admin(name, user_id):
    con = sqlite3.connect('db/admins.db')
    cur = con.cursor()
    res = cur.execute(f"""SELECT name FROM Admins WHERE (name = '{name}' AND id = '{user_id}')""").fetchall()
    if res:
        return True
    else:
        return False
