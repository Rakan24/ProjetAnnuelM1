from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# === Modèles personnalisés ===

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=64, null=True, blank=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)

    def token_valid(self):
        return self.reset_token_expiry and self.reset_token_expiry > timezone.now()

    def __str__(self):
        return f"Profil de {self.user.username}"



# === Tables natives Django utilisées dans le projet ===
# auth_user            : table des utilisateurs (username, email, password, etc.)
# auth_group           : groupes d’utilisateurs pour permissions
# auth_permission      : permissions sur les objets
# django_content_type  : mapping des modèles (content types)
# django_session       : sessions utilisateur (si activées)
# django_migrations    : historique des migrations appliquées
# django_admin_log     : journal des actions dans l’admin Django
