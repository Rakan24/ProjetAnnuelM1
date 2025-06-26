from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Threshold, Prediction
from datetime import date
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny



@api_view(['GET'])
# @authentication_classes([])  # <-- désactive l’authentification sur cette vue
@permission_classes([IsAdminUser])
def get_thresholds(request):

    print("User in request:", request.user)
    print("Is authenticated:", request.user.is_authenticated)
    print("Is staff:", request.user.is_staff)

    try:
        threshold = Threshold.objects.latest('updated_at')  # récupère le plus récent
        data = {
            'pm25': threshold.pm25,
            'pm10': threshold.pm10,
            'o3': threshold.o3,
            'no2': threshold.no2,
        }
        return Response(data)
    except Threshold.DoesNotExist:
        # Aucun seuil défini
        return Response({
            'pm25': None,
            'pm10': None,
            'o3': None,
            'no2': None,
        })


@api_view(['POST'])
# @authentication_classes([])  # <-- désactive l’authentification sur cette vue
@permission_classes([IsAdminUser])  # Tu peux adapter selon tes besoins
def save_thresholds(request):
    data = request.data
    try:
        # Tu peux choisir : remplacer les seuils précédents ou en créer un nouveau
        thresholds = Threshold.objects.last()
        if thresholds:
            thresholds.pm25 = data.get('pm25', thresholds.pm25)
            thresholds.pm10 = data.get('pm10', thresholds.pm10)
            thresholds.o3 = data.get('o3', thresholds.o3)
            thresholds.no2 = data.get('no2', thresholds.no2)
            thresholds.save()
        else:
            thresholds = Threshold.objects.create(
                pm25 = data.get('pm25', 0),
                pm10 = data.get('pm10', 0),
                o3 = data.get('o3', 0),
                no2 = data.get('no2', 0),
            )


        #A supprimer, juste création pour tests !!
        # Ajout : créer ou mettre à jour la prédiction du jour avec toutes les valeurs à 50
        Prediction.objects.update_or_create(
            date=date.today(),
            defaults={
                'pm25': 50,
                'pm10': 50,
                'o3': 50,
                'no2': 50
            }
        )
        return Response({'message': 'Seuils enregistrés avec succès.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': f'Erreur lors de l’enregistrement : {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

