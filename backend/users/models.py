from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=64, null=True, blank=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)

    def token_valid(self):
        return self.reset_token_expiry and self.reset_token_expiry > timezone.now()

    def __str__(self):
        return f"Profil de {self.user.username}"
