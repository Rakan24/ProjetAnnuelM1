import logging
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

class MyTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email_or_username = attrs.get('email') or attrs.get('username')
        password = attrs.get('password')

        print(f"[DEBUG] Tentative login avec : {email_or_username}")
        logger.debug(f"Tentative login avec : {email_or_username}")

        user = None

        # Essayer de trouver par email
        try:
            user = User.objects.get(email=email_or_username)
            print(f"[DEBUG] Utilisateur trouvé par email : {user}")
        except User.DoesNotExist:
            # Essayer de trouver par username
            try:
                user = User.objects.get(username=email_or_username)
                print(f"[DEBUG] Utilisateur trouvé par username : {user}")
            except User.DoesNotExist:
                print(f"[WARNING] Aucun utilisateur trouvé avec : {email_or_username}")
                raise serializers.ValidationError('Identifiants invalides.')

        if not user.check_password(password):
            print(f"[WARNING] Mauvais mot de passe pour : {email_or_username}")
            raise serializers.ValidationError('Mot de passe incorrect.')

        if not user.is_active:
            print(f"[WARNING] Compte inactif pour : {email_or_username}")
            raise serializers.ValidationError('Ce compte est inactif.')

        # Générer le token refresh
        refresh = RefreshToken.for_user(user)

        # Ajouter des claims personnalisées dans le token access
        access_token = refresh.access_token
        access_token['is_staff'] = user.is_staff
        access_token['email'] = user.email
        # Tu peux ajouter d'autres infos si besoin, par ex. access_token['role'] = user.role

        data = {
            'refresh': str(refresh),
            'access': str(access_token),
        }

        print(f"[DEBUG] Token généré avec claims personnalisées : {data}")
        return data
