from django.db import models
from datetime import date


class Threshold(models.Model):
    pm25 = models.FloatField("Seuil PM2.5")
    pm10 = models.FloatField("Seuil PM10")
    o3 = models.FloatField("Seuil O3")
    no2 = models.FloatField("Seuil NO2")
    updated_at = models.DateTimeField(auto_now=True)  # Date de dernière mise à jour

    def __str__(self):
        return f"Seuils (PM2.5: {self.pm25}, PM10: {self.pm10}, O3: {self.o3}, NO2: {self.no2})"



class Prediction(models.Model):
    date = models.DateField("Date de la prédiction")
    pm25 = models.FloatField("PM2.5 prédit")
    pm10 = models.FloatField("PM10 prédit")
    o3 = models.FloatField("O3 prédit")
    no2 = models.FloatField("NO2 prédit")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prédiction du {self.date} (PM2.5: {self.pm25}, PM10: {self.pm10}, O3: {self.o3}, NO2: {self.no2})"



    #A supprimer, juste création pour tests !!
    @staticmethod
    def create_today_test_prediction():
        """Crée une prédiction pour aujourd'hui avec toutes les valeurs à 50."""
        return Prediction.objects.create(
            date=date.today(),
            pm25=50,
            pm10=50,
            o3=50,
            no2=50
        )


# === Tables natives Django utilisées dans le projet ===
# auth_user            : table des utilisateurs (username, email, password, etc.)
# auth_group           : groupes d’utilisateurs pour permissions
# auth_permission      : permissions sur les objets
# django_content_type  : mapping des modèles (content types)
# django_session       : sessions utilisateur (si activées)
# django_migrations    : historique des migrations appliquées
# django_admin_log     : journal des actions dans l’admin Django