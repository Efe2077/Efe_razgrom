import sqlite3


def writing(email, password, name):
    con = sqlite3.connect('blog.db')
    cur = con.cursor()
    res = cur.execute(f"SELECT email_id, password, name FROM Users WHERE email_id = '{email}'").fetchall()
    answer = f'Здравствуйте, {name}'
    if not res:
        cur.execute(f"""INSERT INTO Users(email_id, password, name) 
        VALUES('{email}', '{password}', '{name}')""")
        answer = f"Здравствуйте, {name}, мы рады, что вы к нам присоеденились!"
    con.commit()
    con.close()
    return answer


writing('test@gmail.com', 'asd', 'aboba')
