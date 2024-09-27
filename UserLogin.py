from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserInfo(db.Model):
    id_email = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(10), primary_key=False)

    def __repr__(self):
        return '<UserInfo %r' % self.id_email
