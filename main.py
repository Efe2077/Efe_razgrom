from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from data import db_session
from data.UserLogin import User

from write import writing_sign_in, writing_information

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
        line = request.args
        user_id = line.get('secret-key')
        name = line.get('name')
        return redirect(f'http://127.0.0.1:8080/form?secret-key={user_id}&name={name}')
    else:
        return render_template('start.html')


@app.route('/form', methods=['GET', 'POST'])
def show_info():
    if request.method == 'GET':
        return render_template('/questions.html')
    if request.method == 'POST':
        line = request.args.get('secret-key')
        for user in db_session.create_session().query(User):
            if user.id == line:
                print(user.name)
        return render_template('/start.html')


@app.route('/login', methods=['GET', 'POST'])
def nex():
    if request.method == 'POST':
        email = request.form['id_email']
        password = request.form['password']
        name = request.form['name']

        try:
            user = User()
            user.name = name
            user.email_id = email
            user.password = password
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            return render_template('start.html/?aboba', link=f'Привет, {name}')
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
                return redirect(f'http://127.0.0.1:8080/start?secret-key={User.id}&name={user.id}')

        return render_template('sign in.html', error='Проверьте данные')
    if request.method == 'GET':
        return render_template('sign in.html')


if __name__ == '__main__':
    db_session.global_init("db/blog.db")
    app.run(port=8080, host='127.0.0.1')
