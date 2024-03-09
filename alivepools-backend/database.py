# 数据库操作

from typing import List, Optional
from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from . import db
from .model import Users, Tasks
from datetime import datetime, timedelta
from flask import current_app

bp = Blueprint("database", __name__)


def create_user(email, password) -> Users:
    user = Users(email=email, email_status="verified", password=password)
    db.session.add(user)
    db.session.commit()
    return user


def query_all_users():
    users = Users.query.all()
    return users


def user_exists(email):
    return Users.query.filter_by(email=email).first() is not None


def query_user_by_id(id: int):
    return Users.query.get(id)


def query_user_by_email(email):
    return Users.query.filter_by(email=email).first()


def delete_user(id):
    user = Users.query.get(id)
    if user:
        tasks = Tasks.query.filter_by(user_id=id).all()
        for task in tasks:
            db.session.delete(task)
        db.session.delete(user)
        db.session.commit()
        return True
    return False


def delete_user_by_id(id) -> bool:
    user = Users.query.get(id)
    if user:
        tasks = Tasks.query.filter_by(user_id=id).all()
        for task in tasks:
            db.session.delete(task)
        db.session.delete(user)
        db.session.commit()
        return True
    return False


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
    return task


def query_task_by_id(id) -> Tasks:
    return Tasks.query.get(id)


def query_task_by_id_and_userid(id: str, user_id: int) -> Optional[Tasks]:
    return Tasks.query.filter_by(id=id, user_id=user_id).first()


def query_tasks_by_user_id(id) -> List[Tasks]:
    return Tasks.query.filter_by(user_id=id).order_by(Tasks.created_at.desc()).all()


def add_task(user_id, domain, email, send_frequency, status):
    task = Tasks(
        user_id=user_id,
        domain=domain,
        email=email,
        send_frequency=send_frequency,
        status=status,
    )
    task.last_run_time = datetime.utcnow()
    task.next_run_time = datetime.utcnow() + timedelta(seconds=send_frequency)
    task.created_at = datetime.utcnow()
    db.session.add(task)
    db.session.commit()
    return task


def update_task(id, task_data, user_id):
    task = Tasks.query.filter_by(id=id, user_id=user_id).first()
    if task:
        task.domain = task_data.get("domain", task.domain)
        task.email = task_data.get("email", task.email)
        task.send_frequency = task_data.get("send_frequency", task.send_frequency)
        task.status = task_data.get("status", task.status)
        db.session.commit()
        return True
    return False


def delete_task(id, user_id):
    task = Tasks.query.filter_by(id=id, user_id=user_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return True
    return False
