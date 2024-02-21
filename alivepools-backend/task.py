# 定时任务

from datetime import datetime, timedelta
import time
from flask import Flask, jsonify, request, Blueprint
from .email import send_custom_email
from .model import Tasks
from . import db
from flask import current_app


# Create a blueprint
bp = Blueprint("task", __name__)


# TODO 未调试
def execute_tasks():
    from . import app

    with app.app_context():
        now = datetime.utcnow()
        tasks = Tasks.query.filter(
            Tasks.next_run_time <= now, Tasks.status == "active"
        ).all()

        for task in tasks:
            print(f"Executing task {task.id}")
            send_custom_email(
                "yaoyishi@gmail.com", subject="Task Test", message="This is a test email"
            )

            task.last_run_time = now
            task.next_run_time = now + timedelta(
                seconds=task.send_frequency
            )  # 假设每个任务都是每分钟运行，这应根据task.frequency来计算
            db.session.commit()
