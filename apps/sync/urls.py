# backend/apps/sync/urls.py
from django.urls import path
from .views import (
    CerdaListCreateView, CerdaDetailView, SincronizarCerdasView,
    GrupoEngordaListCreateView, GrupoEngordaDetailView, SincronizarGruposView,
    EventoCalendarioListCreateView, EventoCalendarioDetailView, SincronizarEventosView
)

urlpatterns = [
    # Cerdas
    path('cerdas/', CerdaListCreateView.as_view(), name='cerdas-list'),
    path('cerdas/<int:pk>/', CerdaDetailView.as_view(), name='cerdas-detail'),
    path('sincronizar/cerdas/', SincronizarCerdasView.as_view(), name='sync-cerdas'),
    
    # Grupos
    path('grupos/', GrupoEngordaListCreateView.as_view(), name='grupos-list'),
    path('grupos/<int:pk>/', GrupoEngordaDetailView.as_view(), name='grupos-detail'),
    path('sincronizar/grupos/', SincronizarGruposView.as_view(), name='sync-grupos'),
    
    # Eventos
    path('eventos/', EventoCalendarioListCreateView.as_view(), name='eventos-list'),
    path('eventos/<int:pk>/', EventoCalendarioDetailView.as_view(), name='eventos-detail'),
    path('sincronizar/eventos/', SincronizarEventosView.as_view(), name='sync-eventos'),
]