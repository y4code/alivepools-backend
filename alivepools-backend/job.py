from datetime import datetime, timedelta
import time


# TODO 未调试
def execute_jobs():
    while True:
        now = datetime.utcnow()
        tasks = Tasks.query.filter(Task.next_run_time <= now, Task.status == 'active').all()
        for task in tasks:
            send_custom_email("recipient@example.com", task.title, task.description)
            task.last_run_time = now
            task.next_run_time = now + timedelta(minutes=1)  # 假设每个任务都是每分钟运行，这应根据task.frequency来计算
            db.session.commit()
        time.sleep(60)  # 每60秒检查一次