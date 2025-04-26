from flask import Flask
from .extensions import db
from .routes import api


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    db.init_app(app)

    app.register_blueprint(api)

    return app