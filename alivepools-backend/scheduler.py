# 定时任务的注册和启动

from apscheduler.schedulers.background import BackgroundScheduler

def init_scheduler():
    from .job import execute_jobs
    scheduler = BackgroundScheduler(daemon=True)

    # 注释以启动定时任务
    # scheduler.add_job(execute_jobs, 'interval', seconds=60, max_instances=100)
    # scheduler.start()