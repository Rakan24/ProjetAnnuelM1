from django.urls import path
from .views import register_user, login_user, get_profile, change_password, delete_profile

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('profile/', get_profile, name='profile'),
    path('change-password/', change_password, name='change-password'),
    path('delete-profile/', delete_profile, name='delete-profile'),  # <-- nouvelle route
]