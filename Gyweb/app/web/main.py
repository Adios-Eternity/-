from flask_login import login_user
from sqlalchemy import desc

from Gyweb.app.web import web
from flask import render_template, request, session, jsonify
from Gyweb.app.models.user import User, Device


@web.route('/')
def home():
    islogin = session.get('islogin')
    if islogin == 'true':
        content = session['username']
        if(session['role'] == 1):
            return render_template('home1.html', content=content)
        context = {
            'devices': Device.query.filter_by(Uid=session['Uid']).all()
        }
        L = len(context['devices'])
        Tongji = {'静态节点': 0,'单轨车': 0,'灌溉阀': 0,'施药机': 0}
        for i in context['devices']:
            Tongji[i.class_] += 1
        con= {}
        i=0;
        for device in context['devices']:
            con["device"+str(i)]={"Did":device.Did,"DevEUI":device.DevEUI,"label":device.label,\
                        "net_type":device.net_type,"class_":device.class_, "status":device.status,\
                        "addtime":device.add_time, "Devcontent":device.Devcontent, "longitude":device.longitude,\
                        "latitude":device.latitude}
            i=i+1;

        return render_template('home.html', L=L, Tongji=Tongji,**context, con=con, content=content)
    return render_template('login.html')

@web.route('/call', methods=['GET', 'POST'])
def call():
    context = {
        'devices': Device.query.filter_by(Uid=session['Uid']).all()
    }
    con = []
    for device in context['devices']:
        con.append({"Did": device.Did, "DevEUI": device.DevEUI, "label": device.label, \
                                  "net_type": device.net_type, "class_": device.class_, "status": device.status, \
                                  "addtime": device.add_time, "Devcontent": device.Devcontent,
                                  "longitude": device.longitude, \
                                  "latitude": device.latitude})
    print({"data":con})
    return jsonify({"data": con})

