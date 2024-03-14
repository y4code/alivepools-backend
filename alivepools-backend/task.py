from datetime import datetime, timedelta
from .database import query_due_tasks_by_status
from .email import send_custom_email
from . import db
from .model import Tasks


def execute_tasks(app):
    with app.app_context():
        tasks = query_due_tasks_by_status("active")
        print(f"Executing tasks: {tasks}")
        for task in tasks:
            send_custom_email(
                task.email,
                f"AlivePools: {task.domain} is not available",
                f"Hello, {task.email}! The website {task.domain} is not available for now. Please check it out.",
            )
            print(f"Task {task.id} is executed")
            task.last_run_time = datetime.utcnow()
            db.session.commit()
