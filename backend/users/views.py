from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response  

#------------------------------------------------------------------------#
#                       Methode get user info                            #
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
#                       Methode change password                          #
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
#                       Methode création user                            #
#------------------------------------------------------------------------#
@api_view(['POST'])
@authentication_classes([])  # <-- désactive l’authentification sur cette vue
@permission_classes([AllowAny])
def register_user(request):
    print("Register request data:", request.data)  # Log entrée
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        print("Missing email or password")
        return Response({'error': 'Email et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=email).exists():
        print("User already exists")
        return Response({'error': 'Utilisateur déjà existant'}, status=status.HTTP_400_BAD_REQUEST)

    is_admin = email == 'admin@gmail.com' and password == '1234'

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        is_staff=is_admin
    )
    print(f"User created: {user.username}")

    # Générer token JWT
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        'message': 'Utilisateur créé avec succès',
        'token': access_token,
    }, status=status.HTTP_201_CREATED)


#------------------------------------------------------------------------#
#                       Methode login user                               #
#------------------------------------------------------------------------#


@api_view(['POST'])
@authentication_classes([])  # <-- désactive l’authentification sur cette vue
@permission_classes([AllowAny])
def login_user(request):
    
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
            'message': 'Connexion réussie',
            'token': access_token,
            'is_staff': user.is_staff
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)



#------------------------------------------------------------------------#
#                       Methode delete user                              #
#------------------------------------------------------------------------#
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    user = request.user
    user.delete()
    return Response({'message': 'Profil supprimé avec succès.'}, status=status.HTTP_204_NO_CONTENT)









#------------------------------------------------------------------------#
#                       Forgot password (send reset link)                #
#------------------------------------------------------------------------#
@api_view(['POST'])
@authentication_classes([])  # <-- désactive l’authentification sur cette vue
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email requis'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Aucun utilisateur trouvé avec cet email.'}, status=status.HTTP_400_BAD_REQUEST)

    token = get_random_string(64)
    user.profile.reset_token = token
    user.profile.reset_token_expiry = timezone.now() + timezone.timedelta(hours=1)
    user.profile.save()

    reset_link = f"http://127.0.0.1:3000/reset-password/{token}"

    send_mail(
        'Réinitialisation de mot de passe',
        f'Visitez ce lien pour réinitialiser votre mot de passe : {reset_link}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )

    return Response({'message': 'Un lien de réinitialisation a été envoyé.'}, status=status.HTTP_200_OK)


#------------------------------------------------------------------------#
#                       Check reset token                                #
#------------------------------------------------------------------------#
@api_view(['GET'])
@authentication_classes([])  # <-- désactive l’authentification sur cette vue
@permission_classes([AllowAny])
def check_reset_token(request, token):
    from users.models import Profile
    try:
        profile = Profile.objects.get(reset_token=token, reset_token_expiry__gt=timezone.now())
        return Response({'message': 'Token valide'}, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({'error': 'Token invalide ou expiré'}, status=status.HTTP_400_BAD_REQUEST)


#------------------------------------------------------------------------#
#                       Reset password                                   #
#------------------------------------------------------------------------#
@api_view(['POST'])
@authentication_classes([])  # <-- désactive l’authentification sur cette vue
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
