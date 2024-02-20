# app.py 或 create_app.py
# 基础配置

import os
from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Configuration for your database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://doadmin:AVNS_XZO6vDqdYsFGGBA2G8W@db-mysql-sgp1-19924-do-user-15764718-0.c.db.ondigitalocean.com:25060/defaultdb"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # 初始化 APScheduler 并注册定时任务
    from .scheduler import init_scheduler

    init_scheduler()

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    app.config["JWT_SECRET_KEY"] = "your_secret_key_here"

    jwt = JWTManager(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    bp = Blueprint("my_blueprint", __name__)
    app.register_blueprint(bp)

    from . import domain_api, email, model, database, job, user_api, otp

    app.register_blueprint(domain_api.bp)
    app.register_blueprint(email.bp)
    app.register_blueprint(model.bp)
    app.register_blueprint(database.bp)
    app.register_blueprint(job.bp)
    app.register_blueprint(user_api.bp)
    app.register_blueprint(otp.bp)

    return app


app = create_app()
