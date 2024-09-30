from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from write import writing_sign_in, writing_log_in

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/info')
def show_info():
    return 'lol'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start')
def start():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def nex():
    if request.method == 'POST':
        email = request.form['id_email']
        password = request.form['password']
        name = request.form['name']

        try:
            answer = writing_log_in(email, password, name)
            if answer == 'Почта уже зарегистрирована, введитее другую':
                return render_template('login.html', error=answer)
            else:
                return render_template('start.html', link=answer)
        except Exception:
            print('Ошибка')
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['id_email']
        password = request.form['password']
        name = request.form['name']

        try:
            answer = writing_sign_in(email, password, name)
            if answer == 'Проверьте данные':
                return render_template('sign in.html', error=answer)
            return render_template('start.html', link=answer)
        except Exception:
            print('Ошибка')
    if request.method == 'GET':
        return render_template('sign in.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
