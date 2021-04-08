from flask import Blueprint

web = Blueprint('web', __name__, url_prefix='/')

from Gyweb.app.web import main
from Gyweb.app.web import management
from Gyweb.app.web import device
from Gyweb.app.web import user
from Gyweb.app.web import analysis
from Gyweb.app.web import login
from Gyweb.app.web import register