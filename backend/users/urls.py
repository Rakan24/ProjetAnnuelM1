from django.urls import path
from .views import (
    register_user, login_user, get_profile, change_password, delete_profile,
    forgot_password, reset_password, check_reset_token  # <-- ajout check_reset_token
)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('profile/', get_profile, name='profile'),
    path('change-password/', change_password, name='change-password'),
    path('delete-profile/', delete_profile, name='delete-profile'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('reset-password/<str:token>/', reset_password, name='reset-password'),
    path('check-reset-token/<str:token>/', check_reset_token, name='check-reset-token'),  # <-- optionnel
]

