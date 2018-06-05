"""Creates and configures an application"""


from flask import Flask
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from instance.config import app_config


db = SQLAlchemy()


from app.blueprints.auth import auth
from app.blueprints.docs import documentation
from app.exceptions import handler
from app.controllers import (
    meal_controller, menu_controller,
    menu_item_controller, order_controller,
    notification_controller
)


def create_app(config_name):
    """This will create the application and setup all the 
    other extensions"""

    # initialize flask and jwt
    app = Flask(__name__, instance_relative_config=True)
    jwt = JWTManager(app)

    # load configuration
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(documentation)

    # initialize the database
    db.init_app(app)
    # application exceptions handler
    handler.init_app(app)
    # jwt blacklists handler
    handler.init_jwt(jwt)

    # the API requires the application context
    with app.app_context():
        url_prefix = '/api/v1'
        manager = APIManager(app, flask_sqlalchemy_db=db)
        meal_controller.create_api(manager, url_prefix=url_prefix)
        menu_controller.create_api(manager, url_prefix=url_prefix)
        order_controller.create_api(manager, url_prefix=url_prefix)
        menu_item_controller.create_api(manager, url_prefix=url_prefix)
        notification_controller.create_api(manager, url_prefix=url_prefix)
    return app
