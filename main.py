from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy

from write import check_admin
from make_and_send_file import render_doc, delete_file, render_official_doc

from data import db_session
from data.UserLogin import User
from data.Information import Info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        value = str(request.get_data())
        if '&' in value:
            value = value[value.rfind('&')+1:value.rfind('=')]
        else:
            value = value[2:value.find('=')]

        line = request.args
        user_id = line.get('secret-key')
        name = line.get('name')

        if value == 'make_form':
            return redirect(f'http://127.0.0.1:8080/form?secret-key={user_id}&name={name}')
        if 'redact' in value:
            db_sess = db_session.create_session().query(Info).filter(Info.id == value[6:])
            return render_template(f'redaction.html', info=db_sess)
        if 'download_file' in value:
            db_sess = db_session.create_session().query(Info).filter(Info.id == value[13:]).first()
            render_doc(db_sess.fio, db_sess.post, db_sess.event,
                       db_sess.sch_class, db_sess.quantity, db_sess.when_go,
                       db_sess.place, db_sess.time_go, db_sess.time_now,
                       db_sess.people, db_sess.time_ar, db_sess.id)

            path = f'outputs/{db_sess.id}.docx'
            filename = f'{db_sess.id}.docx'
            return send_file(
                path,
                mimetype='docx',
                download_name=filename,
                as_attachment=True
                )
        if 'save_changes' in value:
            command = [i for i in request.form.keys()][:-1]
            db_sess = db_session.create_session()

            info = db_sess.query(Info).filter(Info.id == value[12:]).first()
            for num, i in enumerate([i for i in request.form.values()][:-1]):
                if i:
                    if command[num] == 'change_fio':
                        info.fio = i
                    elif command[num] == 'change_post':
                        info.post = i
                    elif command[num] == 'change_event':
                        info.event = i
                    elif command[num] == 'change_sch_class':
                        info.sch_class = i
                    elif command[num] == 'change_quantity':
                        info.quantity = i
                    elif command[num] == 'change_when_go':
                        info.when_go = i
                    elif command[num] == 'change_place':
                        info.place = i
                    elif command[num] == 'change_time_go':
                        info.time_go = i
                    elif command[num] == 'change_time_ar':
                        info.time_ar = i
                    elif command[num] == 'change_time_now':
                        info.time_now = i
                    elif command[num] == 'change_people':
                        info.people = i
            db_sess.commit()
            return redirect(f'http://127.0.0.1:8080/start?secret-key={user_id}&name={name}')
        if 'admin_download' in value:
            info = db_session.create_session().query(Info).filter(Info.id == value[14:]).first()
            render_official_doc(info.name, info.sch_class, info.place, info.event,
                                info.when_go, info.time_go, info.time_now, value[14:])

            path = f'outputs_from_admin/{info.id}res_prikaz.docx'
            filename = f'{info.id}res_prikaz.docx'
            return send_file(
                path,
                mimetype='docx',
                download_name=filename,
                as_attachment=True
                )
        else:
            id_of_delete = value[value.find('del')+3:]
            db_sess = db_session.create_session()
            db_sess.query(Info).filter(Info.id == id_of_delete).delete()
            db_sess.commit()
            return redirect(f'http://127.0.0.1:8080/start?secret-key={user_id}&name={name}')
    else:
        value_of_id = request.args.get('secret-key')
        db_sess = db_session.create_session().query(Info)
        db_sess2 = db_session.create_session().query(User)
        name = db_sess2.filter(User.id == int(value_of_id))[0].name
        info = db_sess.filter(Info.user_id == int(value_of_id))
        if check_admin(name):
            for i in db_sess.filter(Info.user_id == value_of_id).all():
                delete_file(i.id, 'outputs_from_admin')
            return render_template('start_for_admin.html', link=f'Привет, {name}', info=db_sess)
        else:
            db_sess3 = db_sess.filter(Info.user_id == value_of_id).all()

            for i in db_sess3:
                delete_file(i.id, 'outputs')

            return render_template('start.html', link=f'Привет, {name}', info=info)


@app.route('/form', methods=['GET', 'POST'])
def show_info():
    if request.method == 'GET':
        return render_template('/questions.html')
    if request.method == 'POST':
        line = request.args.get('secret-key')
        for user in db_session.create_session().query(User):
            if user.id == int(line):
                info = Info()
                info.fio = request.form['fio']
                info.post = request.form['post']
                info.event = request.form['event']
                info.sch_class = request.form['sch_class']
                info.quantity = request.form['quantity']
                info.when_go = request.form['when_go']
                info.place = request.form['place']
                info.time_go = request.form['time_go']
                info.time_ar = request.form['time_ar']
                info.time_now = request.form['time_now']
                info.people = request.form['people']
                info.user_id = user.id
                info.name = user.name

                db_sess = db_session.create_session()
                db_sess.add(info)
                db_sess.commit()
                return redirect(f'http://127.0.0.1:8080/start?secret-key={line}&name={user.name}')
        return render_template('start.html')


@app.route('/login', methods=['GET', 'POST'])
def nex():
    if request.method == 'POST':
        email = request.form['id_email']
        password = request.form['password']
        name = request.form['name']
        user = User()
        user.name = name
        user.email_id = email
        user.password = password
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        try:
            return redirect(f'http://127.0.0.1:8080/start?secret-key={user.id}&name={user.name}')
        except Exception:
            return render_template('login.html', error='Почта уже используется')
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['id_email']
        password = request.form['password']

        db_sess = db_session.create_session()
        for user in db_sess.query(User):
            if email == user.email_id and password == user.password:
                return redirect(f'http://127.0.0.1:8080/start?secret-key={user.id}&name={user.name}')

        return render_template('sign in.html', error='Проверьте данные')
    if request.method == 'GET':
        return render_template('sign in.html')


if __name__ == '__main__':
    db_session.global_init("db/blog.db")
    app.run(port=8080, host='127.0.0.1')

