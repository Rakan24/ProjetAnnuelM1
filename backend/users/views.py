from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import update_session_auth_hash
from rest_framework.permissions import AllowAny


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
    update_session_auth_hash(request, user)  # <-- pour ne pas déconnecter après changement

    return Response({'message': 'Mot de passe mis à jour avec succès'})


#------------------------------------------------------------------------#
#                       Methode création user                            #
#------------------------------------------------------------------------#
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    print(request.data)  # pour debug

    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=email).exists():
        return Response({'error': 'Utilisateur déjà existant'}, status=status.HTTP_400_BAD_REQUEST)
    



    # Création rapide de l'admin si email et password correspondent à ce que tu veux
    if email == 'admin@gmail.com' and password == '1234':
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            is_staff=True  # <-- Admin
        )
        return Response({'message': 'Admin créé avec succès'}, status=status.HTTP_201_CREATED)
    


    

    # Création utilisateur normal
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        is_staff=False  # utilisateur simple
    )

    return Response({'message': 'Utilisateur créé avec succès'}, status=status.HTTP_201_CREATED)





#------------------------------------------------------------------------#
#                       Methode login user                               #
#------------------------------------------------------------------------#
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')


    #------------------------------------ Pour débug ------------------------------------#
    # print(f"Email: {email}")
    # print(f"Password: {password}")
    # user = authenticate(username=email, password=password)
    # print(f"User: {user}")
    #------------------------------------ Fin débug ------------------------------------#
    
    if not email or not password:
        return Response({'error': 'Email et mot de passe requis'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)  # ⬅️ génère un token si non existant
        return Response({
            'message': 'Connexion réussie',
            'token': token.key,
            'is_staff': user.is_staff  # 👈 utile pour afficher différemment côté frontend
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


