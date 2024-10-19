import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'Users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email_id = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    info = orm.relationship('Info', back_populates='user')
