from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

from UserLogin import UserInfo
from write import writing

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
            answer = writing(email, password, name)
            return render_template('start.html', link=answer)
        except Exception:
            print('Ошибка')
    if request.method == 'GET':
        return render_template('login.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
