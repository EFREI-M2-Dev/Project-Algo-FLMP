import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from app.services import init_service
import subprocess

def job():
    print("Updating the dataset...")
    subprocess.run(["python", "-m", "app.services.train_service"], check=True)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', minutes=1)  # Toutes les 1 minute
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())
