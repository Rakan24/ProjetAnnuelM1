from datetime import datetime
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model
from utils.email import send_email
from predictions.models import Threshold, Prediction
import sys


def check_thresholds_and_notify():
    try:

        print(f"⌚ Cron lancé à {datetime.now()}", file=sys.stdout, flush=True)

        now = datetime.now()
        start_of_day = make_aware(datetime(now.year, now.month, now.day, 0, 0, 0))
        end_of_day = make_aware(datetime(now.year, now.month, now.day, 23, 59, 59))

        thresholds = Threshold.objects.first()  # ou filtre par admin s’il y en a plusieurs
        if not thresholds:
            print("⚠️ Aucun seuil défini", flush=True)
            return

        # Récupérer les prédictions du jour
        predictions = Prediction.objects.filter(date=now.date())
        if not predictions.exists():
            print("ℹ️ Aucune prédiction pour aujourd'hui", flush=True)
            return

        exceeded = {}
        for prediction in predictions:
            if prediction.pm25 > thresholds.pm25:
                exceeded['PM2.5'] = f"{prediction.pm25} (seuil: {thresholds.pm25})"
            if prediction.pm10 > thresholds.pm10:
                exceeded['PM10'] = f"{prediction.pm10} (seuil: {thresholds.pm10})"
            if prediction.o3 > thresholds.o3:
                exceeded['O3'] = f"{prediction.o3} (seuil: {thresholds.o3})"
            if prediction.no2 > thresholds.no2:
                exceeded['NO2'] = f"{prediction.no2} (seuil: {thresholds.no2})"

        if exceeded:
            print(f"🚨 Dépassements détectés : {exceeded}", flush=True)
            notify_users(exceeded)
        else:
            print("✅ Aucun dépassement détecté", flush=True)

    except Exception as e:
        print(f"❌ Erreur dans la vérification des seuils : {e}", flush=True)

def notify_users(exceeded):
    User = get_user_model()
    users = User.objects.all()

    subject = "🚨 Alerte dépassement des seuils"
    text = "Les valeurs suivantes ont dépassé les seuils définis aujourd'hui :\n"
    text += "\n".join([f"{k} : {v}" for k, v in exceeded.items()])
    text += "\n\nMerci de prendre les mesures nécessaires."

    html = f"<p>Les valeurs suivantes ont dépassé les seuils définis aujourd'hui :</p><ul>"
    html += "".join([f"<li><strong>{k}</strong> : {v}</li>" for k, v in exceeded.items()])
    html += "</ul><p>Merci de prendre les mesures nécessaires.</p>"

    for user in users:
        send_email(user.email, subject, text, html)
