import os
from flask import Flask
from infrastructure.flask_app.configs import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True, instance_path=os.path.dirname(__file__))
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('configs.py')

    from application import product_blueprint
    app.register_blueprint(product_blueprint)

    return app
