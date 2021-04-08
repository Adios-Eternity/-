from Gyweb.app.web import web
from flask import render_template, request, make_response, redirect, url_for, session
from Gyweb.app.web.upic import ImageCode, gen_email_code, send_email
from Gyweb.app.models.base import db
from Gyweb.app.models.user import User, Device

@web.route('/register_m')
def register_m():
    return render_template('register.html')


@web.route('/vcode')
def vcode():
    code, bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response

icode = {}

@web.route('/ecode', methods=['GET', 'POST'])
def ecode():
    username = request.form.get('username')
    password = request.form.get('password')
    rpassword = request.form.get('rpassword')
    email = request.form.get('email')
    un = User.query.filter_by(username=username).all()
    if un != []:
        return "username-fail"
    if password !=rpassword:
        return "password-fail"
    code = gen_email_code()
    icode["code"] = code
    try:
        send_email(email, code)
        return 'send-pass'
    except:
        return 'send-fail'

@web.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    tel = request.form.get('tel')
    email = request.form.get('email')
    code = request.form.get('code')
    if icode["code"] == code:
        print()
        user = User(username=username, password=password, email=email, tele=tel, role=0)
        db.session.add(user)
        db.session.commit()
        return "register-pass"
    else:
        return "register-fail"