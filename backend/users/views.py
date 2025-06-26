from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response  

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from utils.email import send_email


#------------------------------------------------------------------------#
# Login avec SimpleJWT + custom serializer
#------------------------------------------------------------------------#
class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("🚀 CustomLoginView POST appelée", flush=True)
        print("Corps reçu :", request.data, flush=True)

        serializer = MyTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            print("❌ Erreurs de validation :", serializer.errors, flush=True)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


#------------------------------------------------------------------------#
# Register user
#------------------------------------------------------------------------#
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=email).exists():
        return Response({'error': 'Utilisateur déjà existant'}, status=status.HTTP_400_BAD_REQUEST)

    is_admin = email == 'admin@gmail.com' and password == '1234'

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        is_staff=is_admin
    )

    # Envoi du mail de bienvenue
    subject = "Bienvenue sur BreathWell !"
    message = (
        f"Bonjour {email},\n\n"
        "Bienvenue sur BreathWell ! Votre compte a bien été créé.\n"
        "Vous pouvez dès à présent vous connecter et profiter de nos services.\n\n"
        "L'équipe BreathWell"
    )
    html_message = f"<p>Bonjour {email},</p><p>Bienvenue sur <strong>BreathWell</strong> ! Votre compte a bien été créé.<br>Vous pouvez dès à présent vous connecter et profiter de nos services.</p><p>L'équipe BreathWell</p>"
    send_email(email, subject, message, html_message)

    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'Utilisateur créé avec succès',
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)

#------------------------------------------------------------------------#
# Get profile
#------------------------------------------------------------------------#
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    return Response({
        'email': user.email,
        'is_staff': user.is_staff,
    })

#------------------------------------------------------------------------#
# Change password
#------------------------------------------------------------------------#
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({'error': 'Ancien mot de passe incorrect'}, status=status.HTTP_400_BAD_REQUEST)

    if not new_password or len(new_password) < 4:
        return Response({'error': 'Le nouveau mot de passe est trop court'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'message': 'Mot de passe mis à jour avec succès'})

#------------------------------------------------------------------------#
# Delete profile
#------------------------------------------------------------------------#
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    user = request.user
    user.delete()
    return Response({'message': 'Profil supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)

#------------------------------------------------------------------------#
# Forgot password
#------------------------------------------------------------------------#
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email requis'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        print(f"[FORGOT PASSWORD] Aucun utilisateur trouvé avec l'email : {email}", flush=True)
        return Response({'error': 'Aucun utilisateur trouvé avec cet email.'}, status=status.HTTP_400_BAD_REQUEST)

    token = get_random_string(64)
    print(f"[FORGOT PASSWORD] Génération du token : {token}", flush=True)
    print(f"[FORGOT PASSWORD] Utilisateur : {user.username} (id={user.id})", flush=True)
    print(f"[FORGOT PASSWORD] Profile avant : token={getattr(user.profile, 'reset_token', None)}, expiry={getattr(user.profile, 'reset_token_expiry', None)}", flush=True)
    user.profile.reset_token = token
    user.profile.reset_token_expiry = timezone.now() + timezone.timedelta(hours=1)
    user.profile.save()
    print(f"[FORGOT PASSWORD] Profile après : token={user.profile.reset_token}, expiry={user.profile.reset_token_expiry}", flush=True)

    reset_link = f"http://127.0.0.1:3000/reset-password/{token}"
    print(f"[FORGOT PASSWORD] Lien envoyé : {reset_link}", flush=True)
    send_mail(
        'Réinitialisation de mot de passe',
        f'Visitez ce lien pour réinitialiser votre mot de passe : {reset_link}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )

    return Response({'message': 'Un lien de réinitialisation a été envoyé.'}, status=status.HTTP_200_OK)

#------------------------------------------------------------------------#
# Check reset token
#------------------------------------------------------------------------#
@api_view(['GET'])
@permission_classes([AllowAny])
def check_reset_token(request, token):
    from users.models import Profile
    print(f"[CHECK TOKEN] Token reçu : {token}", flush=True)
    try:
        profile = Profile.objects.get(reset_token=token, reset_token_expiry__gt=timezone.now())
        print(f"[CHECK TOKEN] Token trouvé pour user : {profile.user.username} (id={profile.user.id})", flush=True)
        return Response({'message': 'Token valide'}, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        print(f"[CHECK TOKEN] Token NON trouvé ou expiré : {token}", flush=True)
        return Response({'error': 'Token invalide ou expiré'}, status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------------------------------------#
# Reset password
#------------------------------------------------------------------------#
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, token):
    new_password = request.data.get('new_password')
    if not new_password or len(new_password) < 4:
        return Response({'error': 'Mot de passe trop court'}, status=status.HTTP_400_BAD_REQUEST)

    from users.models import Profile
    try:
        profile = Profile.objects.get(reset_token=token, reset_token_expiry__gt=timezone.now())
        user = profile.user
        user.set_password(new_password)
        user.save()
        profile.reset_token = None
        profile.reset_token_expiry = None
        profile.save()
        return Response({'message': 'Mot de passe réinitialisé avec succès'}, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({'error': 'Token invalide ou expiré'}, status=status.HTTP_400_BAD_REQUEST)
