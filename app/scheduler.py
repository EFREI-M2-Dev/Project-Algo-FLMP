import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

def job():
    subprocess.run(["python", "-m", "app.services.reinforcement"], check=True)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', weeks=1)  # Toutes les semaines
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())
