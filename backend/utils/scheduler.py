from apscheduler.schedulers.background import BackgroundScheduler
from utils.alerts import check_thresholds_and_notify

scheduler_instance = None

def start_scheduler():
    global scheduler_instance
    if scheduler_instance is None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(check_thresholds_and_notify, 'interval', minutes=5)
        scheduler.start()
        scheduler_instance = scheduler
        print("✅ Scheduler démarré, vérification des seuils toutes les 5 minutes", flush=True)
    else:
        print("⚠️ Scheduler déjà en cours", flush=True)