import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from infrastructure.flask_app.configs import app_config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True, instance_path=os.path.dirname(__file__))
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('configs.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    Migrate(app, db)

    from infrastructure import models

    from application.product import product_blueprint
    app.register_blueprint(product_blueprint)

    return app
