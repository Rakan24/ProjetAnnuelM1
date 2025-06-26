from django.apps import AppConfig
import sys
import os

class PredictionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictions'

    def ready(self):
        if ('runserver' in sys.argv or 'runworker' in sys.argv) and os.environ.get('RUN_MAIN') == 'true':
            from utils.scheduler import start_scheduler
            start_scheduler()
