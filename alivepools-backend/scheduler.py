from .task import execute_tasks
from apscheduler.schedulers.background import BackgroundScheduler


def init_scheduler(app):
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        func=execute_tasks, args=(app,), trigger="interval", seconds=60, max_instances=1
    )
    scheduler.start()
