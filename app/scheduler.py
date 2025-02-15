import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from app.services import init_service, train_service, main
import time

def job():
    print("Updating the dataset...")
    init_service.import_data()
    train_service.train_model()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', minutes=1)  # Toutes les 1 minute
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())
