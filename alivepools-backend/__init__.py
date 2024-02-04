# app.py 或 create_app.py

import os
from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
from .job import execute_jobs

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'

    jwt = JWTManager(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    bp = Blueprint('my_blueprint', __name__)
    app.register_blueprint(bp)

    from . import auth, domain, email
    app.register_blueprint(auth.bp)
    app.register_blueprint(domain.bp)
    app.register_blueprint(email.bp)

    # 初始化 APScheduler 并注册定时任务
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(execute_jobs, 'interval', minutes=1)
    scheduler.start()

    return app

app = create_app()
