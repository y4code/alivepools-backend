# 数据库操作

from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from . import db
from .model import Users, Tasks
from datetime import datetime, timedelta
from flask import current_app

bp = Blueprint("database", __name__)


def create_user(email, password):
    user = Users(email=email, email_status="verified", password=password)
    db.session.add(user)
    db.session.commit()
    return user


def query_all_users():
    users = Users.query.all()
    return users, 200


def user_exists(email):
    user = Users.query.filter_by(email=email).first()
    if user:
        return True
    return False


def query_user_by_id(id):
    user = Users.query.get_or_404(id)
    return user, 200


def query_user_by_email(email):
    user = Users.query.filter_by(email=email).first()
    return user, 200


def delete_user(id):
    user = Users.query.get_or_404(id)
    tasks = Tasks.query.filter_by(user_id=id).all()
    for task in tasks:
        db.session.delete(task)
    db.session.delete(user)
    db.session.commit()
    return user, 200


def create_task(user_id, domain, email, send_frequency, status):
    task = Tasks(
        user_id=user_id,
        domain=domain,
        email=email,
        send_frequency=send_frequency,
        status=status,
    )
    task.last_run_time = datetime.utcnow()
    task.next_run_time = datetime.utcnow() + timedelta(seconds=send_frequency)
    db.session.add(task)
    db.session.commit()
    return task, 201


def query_tasks_by_user_id(id):
    tasks = Tasks.query.filter_by(user_id=id).all()
    tasks_list = []
    for task in tasks:
        tasks_list.append(
            {
                "domain": task.domain,
                "email": task.email,
                "send_frequency": task.send_frequency,
                "created_at": task.created_at,
                "status": task.status,
                "last_run_time": task.last_run_time,
                "next_run_time": task.next_run_time,
            }
        )
    return tasks_list, 200


def delete_task(id):
    task = Tasks.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return task, 200
