from flask_login import login_user
from Gyweb.app.web.tcpsocket import socketserver
from Gyweb.app.web.socket_server import connect
from Gyweb.app.web import web
from flask import render_template, request, jsonify, redirect, url_for, session

from Gyweb.app.models.user import User, Device


@web.route('/net_debugger')
def net_debugger():
    content = session['username']
    return render_template('debugger.html', content=content)

@web.route('/net_send', methods=['GET', 'POST'])
def net_send():
    message = request.form.get('message')
    content = {"flag": 1, "data": message}
    print(socketserver(content).callback_data())

    return "send-pass"

@web.route('/control_panel')
def control_panel():
    content = session['username']
    context = {
        'devices': Device.query.filter_by(Uid=session['Uid']).limit(6).offset(0).all()
    }
    return render_template('control-panel.html', **context, content=content)

@web.route('/control_list/<Start>',methods=['GET', 'POST'])
def control_list(Start):
    context = {
        'devices': Device.query.filter_by(Uid=session['Uid']).limit(6).offset(Start).all()
    }
    content = session['username']
    return render_template('control-panel.html', **context, content=content)