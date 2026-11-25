# backend/apps/payments/urls.py
from django.urls import path
from .views import (
    CrearIntentoPagoView, StripeWebhookView, HistorialPagosView
)

urlpatterns = [
    path('crear-intento/', CrearIntentoPagoView.as_view(), name='crear-intento'),
    path('webhook/stripe/', StripeWebhookView.as_view(), name='webhook-stripe'),
    path('historial/', HistorialPagosView.as_view(), name='historial-pagos'),
]