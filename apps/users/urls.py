# backend/apps/users/urls.py
from django.urls import path
from .views import RegisterView, LoginView, VerificarSuscripcionView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verificar-suscripcion/', VerificarSuscripcionView.as_view(), name='verificar-suscripcion'),
    path('logout/', LogoutView.as_view(), name='logout'),
]