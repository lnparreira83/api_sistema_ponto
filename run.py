from flask import Flask
from flask_restful import Api
import sys

from api_sistema_ponto.app import app


def create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile('../config/' + config + '.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api = Api(app)

    api.init_app(api)
    return app


app.run()
