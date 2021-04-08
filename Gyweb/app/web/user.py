from Gyweb.app.web import web
from flask import render_template, request, jsonify, redirect, url_for, session

from Gyweb.app.models.base import db
from Gyweb.app.models.user import User, Device


@web.route('/user_m/<start>')
def user_m(start):
    context = {
        'users': User.query.limit(6).offset(start).all()
    }
    content = session['username']
    return render_template('user.html', **context, content=content)

@web.route('/manageuser')
def manageuser():
    content = session['username']
    return render_template('manageuser.html', content=content)


@web.route('/user_add', methods=['GET', 'POST'])
def user_add():
    if request.method == 'GET':
        return 'post plz'
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        tele = request.form.get('tele')
        role = request.form.get('role')
    user = User(username=username, password=password, email=email, tele=tele, role=role)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('web.user_m'))



@web.route('/user_delete/<Uid>')
def user_delete(Uid):
    device = Device.query.filter_by(Uid=Uid).all()
    for i in device:
        db.session.delete(i)
        db.session.commit()
    user = User.query.filter_by(Uid=Uid).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('web.user_m'))

@web.route('/user_modify', methods=['GET', 'POST'])
def user_modify():
    if request.method == 'GET':
        'post plz'
    else:
        Uid = request.form.get('Uid')
        username = request.form.get('m_username')
        password = request.form.get('m_password')
        email = request.form.get('m_email')
        tele = request.form.get('m_tele')
        role = request.form.get('m_role')
        print(Uid,username,password,email,tele,role)
    user = User.query.filter_by(Uid=Uid).first()
    user.username = username
    user.password = password
    user.email = email
    user.tele = tele
    user.role = role
    db.session.commit()
    return redirect(url_for('web.user_m'))

