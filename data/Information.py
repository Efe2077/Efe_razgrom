import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Info(SqlAlchemyBase):
    __tablename__ = 'Info'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    fio = sqlalchemy.Column(sqlalchemy.String, index=True, unique=False, nullable=True)
    post = sqlalchemy.Column(sqlalchemy.String, index=True, unique=False, nullable=True)
    event = sqlalchemy.Column(sqlalchemy.String, index=True, unique=False, nullable=True)
    sch_class = sqlalchemy.Column(sqlalchemy.String, index=True, unique=False, nullable=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, index=True, unique=False, nullable=True)
    when_go = sqlalchemy.Column(sqlalchemy.Date, index=True, unique=False, nullable=True)
    place = sqlalchemy.Column(sqlalchemy.String, index=True, unique=False, nullable=True)
    time_ar = sqlalchemy.Column(sqlalchemy.String, index=True, unique=False, nullable=True)
    time_go = sqlalchemy.Column(sqlalchemy.String, index=True, unique=False, nullable=True)
    time_now = sqlalchemy.Column(sqlalchemy.Date, index=True, unique=False, nullable=True)
    people = sqlalchemy.Column(sqlalchemy.String, index=True, unique=False, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("Users.id"))

    user = orm.relationship('User')

    def __repr__(self):
        return self.id, self.fio, self.post, self.event
