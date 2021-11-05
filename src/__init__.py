from flask_apispec import FlaskApiSpec
from flask_restful import Api
from src.utils.jwt import JWT

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


from flask.app import Flask
from config import Config, ConfigNames

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWT()

from src.utils.register_endpoints import register_api_endpoints, register_docs


def create_app(config: Config = ConfigNames.DEVELOPMENT) -> Flask:
    app = Flask(__name__, instance_relative_config=True, )
    app.config.from_object(config.value)
    app.config['JWT_SECRET_KEY'] = 'super-secret'

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    docs = FlaskApiSpec(app)

    register_api_endpoints(api)
    register_docs(docs)
    return app
