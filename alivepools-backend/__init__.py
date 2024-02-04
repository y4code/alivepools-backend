import os
from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager, create_access_token

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'

    # Initialize JWTManager
    jwt = JWTManager(app)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Create a blueprint
    bp = Blueprint('my_blueprint', __name__)

    # Register the blueprint
    app.register_blueprint(bp)
    
    return app