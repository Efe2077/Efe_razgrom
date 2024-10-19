import sqlite3


def writing_sign_in(email, password, name):
    con = sqlite3.connect('db/blog.db')
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
    con = sqlite3.connect('db/blog.db')
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


def writing_information(lst):
    con = sqlite3.connect('db/info.db')
    cur = con.cursor()
    res = cur.execute(f"SELECT fio FROM Info WHERE fio = '{lst[0]}'").fetchall()
    if not res:
        cur.execute(f"""INSERT INTO Info(fio, post, event, sch_class,
                        quantity, when_go, place, time_go, time_ar, time_now, people)
                        VALUES('{lst[0]}', '{lst[1]}', '{lst[2]}', '{lst[3]}', '{lst[4]}', '{lst[5]}',
                        '{lst[6]}', '{lst[7]}', '{lst[8]}', '{lst[9]}', '{lst[10]}')
                        """).fetchall()
        con.commit()
        con.close()
    else:
        print('Заявка уже есть, просмотрите ее или измените')
