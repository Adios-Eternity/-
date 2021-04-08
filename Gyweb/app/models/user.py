from Gyweb.app import login_manager
from Gyweb.app.models.base import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    Uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40))
    tele = db.Column(db.String(11))
    role = db.Column(db.Integer, nullable=False)


# 需要提供一个user_loader回调。此回调用于从会话中存储的用户ID重新加载用户对象。它应该unicode带有用户的ID，并返回相应的用户对象:
@login_manager.user_loader
def get_user(Uid):
    return User.query.get(int(Uid))


class Device(db.Model):
    __tablename__ = 'device'
    Did = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DevEUI = db.Column(db.String(40))
    label = db.Column(db.String(20))
    net_type = db.Column(db.String(20))
    class_ = db.Column(db.String(20))
    status = db.Column(db.Integer)
    add_time = db.Column(db.DATETIME)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    Devcontent = db.Column(db.String(255))
    Uid = db.Column(db.Integer, db.ForeignKey('user.Uid'))


class Gateway(db.Model):
    __tablename__ = 'gateway'
    Gid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    GEUI = db.Column(db.String(100))
    serverhost = db.Column(db.String(100))
    serverport = db.Column(db.Integer)
    frequency = db.Column(db.String(100))
    tspeed = db.Column(db.String(100))
    addtime = db.Column(db.DATETIME)