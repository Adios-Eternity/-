from Gyweb.app.web import web
from flask import render_template, request, jsonify, redirect, url_for, session

from Gyweb.app.models.base import db
from Gyweb.app.models.user import User, Device, Gateway


@web.route('/device_m')
def device_m():
    context = {
        'devices': Device.query.filter_by(Uid=session['Uid']).limit(6).offset(0).all()
    }
    content = session['username']
    return render_template('device.html', **context, content=content)

@web.route('/gateway_m')
def gateway_m():
    context = {
        'macs': Gateway.query.all()
    }
    content = session['username']
    return render_template('gateway_setting.html', **context, content=content)

@web.route('/gateway_delete/<Gid>')
def gateway_delete(Gid):
    device = Gateway.query.filter_by(Gid=Gid).first()
    db.session.delete(device)
    db.session.commit()
    return redirect(url_for('web.gateway_m'))

@web.route('/gateway_add',methods=['GET', 'POST'])
def gateway_add():
    if request.method == 'GET':
        return 'post plz'
    else:
        GEUI = request.form.get('GEUI')
        serverhost = request.form.get('serverhost')
        serverport = request.form.get('serverport')
        frequency = request.form.get('frequency')
        tspeed = request.form.get('tspeed')
        addtime = request.form.get('addtime')

    gateway = Gateway(GEUI=GEUI, serverhost=serverhost, serverport=serverport, frequency=frequency, tspeed=tspeed, addtime=addtime)
    db.session.add(gateway)
    db.session.commit()
    return redirect(url_for('web.gateway_m'))

@web.route('/device_list/<Start>', methods=['GET', 'POST'])
def device_list(Start):
    context = {
        'devices': Device.query.filter_by(Uid=session['Uid']).limit(6).offset(Start).all()
    }
    content = session['username']
    return render_template('device.html', **context, content=content)


@web.route('/device_modify', methods=['GET', 'POST'])
def device_modify():
    if request.method == 'GET':
        'post plz'
    else:
        Did = request.form.get('Did')
        DevEUI = request.form.get('DevEUI')
        label = request.form.get('label')
        net_type = request.form.get('net_type')
        class_ = request.form.get('class_')
        Status = request.form.get('status')
        if Status == "有效":
            status = 1
        else:
            status = 0
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')
        add_time = request.form.get('add_time')
        Devcontent = request.form.get('Devcontent')

    device = Device.query.filter_by(Did=Did).first()
    device.DevEUI = DevEUI
    device.label = label
    device.net_type = net_type
    device.class_ = class_
    device.status = status
    device.longitude = longitude
    device.latitude = latitude
    if add_time is not '':
        device.add_time = add_time
    device.Devcontent = Devcontent
    db.session.commit()
    return redirect(url_for('web.device_m'))


@web.route('/device_add', methods=['GET', 'POST'])
def device_add():
    if request.method == 'GET':
        return 'post plz'
    else:
        DevEUI = request.form.get('DevEUI')
        label = request.form.get('label')
        net_type = request.form.get('net_type')
        class_ = request.form.get('class_')
        Status = request.form.get('status')
        if Status == "有效":
            status = 1
        else:
            status = 0
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')
        add_time = request.form.get('add_time')
        Devcontent = request.form.get('Devcontent')
        Uid = request.form.get('Uid')
    device = Device(DevEUI=DevEUI, label=label, net_type=net_type, class_=class_, status=status,longitude=longitude, latitude=latitude, add_time=add_time,Devcontent=Devcontent , Uid=Uid)
    db.session.add(device)
    db.session.commit()
    return redirect(url_for('web.device_m'))



@web.route('/device_delete/<Did>')
def device_delete(Did):
    device = Device.query.filter_by(Did=Did).first()
    db.session.delete(device)
    db.session.commit()
    return redirect(url_for('web.device_m'))