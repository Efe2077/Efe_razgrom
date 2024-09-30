import sqlite3


def writing_sign_in(email, password, name):
    con = sqlite3.connect('blog.db')
    cur = con.cursor()
    res = cur.execute(f"SELECT email_id, password, name FROM Users WHERE email_id = '{email}' "
                      f"AND password = '{password}' AND name = '{name}'").fetchall()
    con.commit()
    con.close()
    if res:
        return f"Здравствуйте, {name}"
    else:
        return f"Проверьте данные"


def writing_log_in(email, password, name):
    con = sqlite3.connect('blog.db')
    cur = con.cursor()
    res = cur.execute(f"SELECT email_id, password, name FROM Users WHERE email_id = '{email}'").fetchall()
    if res:
        return 'Почта уже зарегистрирована, введитее другую'
    else:
        cur.execute(f"""INSERT INTO Users(email_id, password, name) 
        VALUES('{email}', '{password}', '{name}')""")
        con.commit()
        con.close()
        return f"Здравствуйте, {name}, мы рады, что вы к нам присоеденились!"

