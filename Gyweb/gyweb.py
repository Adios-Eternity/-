from Gyweb.app.models.base import db
from Gyweb.app import create_app
__author__ = 'zzy'
 

app = create_app()

db.create_all(app=app)


if __name__ == '__main__':
    # db.create_all(app=app)
    app.run(debug=app.config['DEBUG'], threaded=True)
