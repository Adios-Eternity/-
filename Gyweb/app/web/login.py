from Gyweb.app.web import web
from flask import render_template, request, jsonify, redirect, url_for, session

from Gyweb.app.models.base import db
from Gyweb.app.models.user import User, Device


@web.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user_login = User.query.all()
    for userlo in user_login:
        if userlo.username == username and userlo.password == password:
            session['islogin'] = 'true'
            session['Uid'] = userlo.Uid
            session['username'] = userlo.username
            session['password'] = userlo.password
            session['role'] = userlo.role
            return "login-pass"
    return "login-fail"

@web.route('/loginout')
def loginout():
    session.clear()
    return redirect(url_for('web.home'))
