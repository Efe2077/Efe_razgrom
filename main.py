from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from write import check_admin

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
        value = value[2:value.find('=')]
        line = request.args
        user_id = line.get('secret-key')
        name = line.get('name')
        if value == 'make_form':
            return redirect(f'http://127.0.0.1:8080/form?secret-key={user_id}&name={name}')
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
            return render_template('start.html', link=f'Привет, {name}', info=db_sess)
        else:
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
