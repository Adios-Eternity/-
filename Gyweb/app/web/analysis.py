from flask_login import login_user
from sqlalchemy import desc

from Gyweb.app.web import web
from flask import render_template, request, session
from Gyweb.app.models.user import User


@web.route('/data_analysis')
def data_analysis():
    content = session['username']
    print(content)
    if session['role'] == 1:
        return render_template('data_analysis1.html', content=content)
    else:
        return render_template('data_analysis.html', content=content)
