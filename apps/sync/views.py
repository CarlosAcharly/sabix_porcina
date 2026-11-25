# backend/apps/sync/views.py
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Cerda, GrupoEngorda, EventoCalendario
from .serializers import (
    CerdaSerializer, GrupoEngordaSerializer, EventoCalendarioSerializer
)

# ----- Vistas para Cerdas -----
class CerdaListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CerdaSerializer
    
    def get_queryset(self):
        return Cerda.objects.filter(
            usuario=self.request.user,
            eliminado=False
        )
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class CerdaDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CerdaSerializer
    
    def get_queryset(self):
        return Cerda.objects.filter(
            usuario=self.request.user
        )
    
    def perform_destroy(self, instance):
        instance.eliminado = True
        instance.sincronizado = False
        instance.save()

class SincronizarCerdasView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CerdaSerializer
    
    def post(self, request):
        usuario = request.user
        data = request.data
        
        with transaction.atomic():
            # Procesar datos entrantes
            if isinstance(data, list):
                for item in data:
                    self.procesar_cerda(usuario, item)
            else:
                self.procesar_cerda(usuario, data)
            
            # Devolver datos actualizados del servidor
            cerdas = Cerda.objects.filter(
                usuario=usuario,
                eliminado=False
            )
            serializer = self.get_serializer(cerdas, many=True)
            
            return Response(serializer.data)
    
    def procesar_cerda(self, usuario, data):
        id_local = data.get('id_local')
        
        if data.get('eliminado', False):
            Cerda.objects.filter(
                usuario=usuario,
                id_local=id_local
            ).update(eliminado=True, sincronizado=True)
            return
        
        defaults = {
            'arete': data.get('arete'),
            'nombre': data.get('nombre'),
            'caracteristicas': data.get('caracteristicas'),
            'fecha_nacimiento': data.get('fecha_nacimiento'),
            'estado': data.get('estado', 'vacia'),
            'corral_id': data.get('corral_id'),
            'sincronizado': True,
            'eliminado': False
        }
        
        Cerda.objects.update_or_create(
            usuario=usuario,
            id_local=id_local,
            defaults=defaults
        )

# ----- Vistas para Grupos de Engorda -----
class GrupoEngordaListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GrupoEngordaSerializer
    
    def get_queryset(self):
        return GrupoEngorda.objects.filter(
            usuario=self.request.user,
            eliminado=False
        )
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class GrupoEngordaDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GrupoEngordaSerializer
    
    def get_queryset(self):
        return GrupoEngorda.objects.filter(
            usuario=self.request.user
        )
    
    def perform_destroy(self, instance):
        instance.eliminado = True
        instance.sincronizado = False
        instance.save()

class SincronizarGruposView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GrupoEngordaSerializer
    
    def post(self, request):
        usuario = request.user
        data = request.data
        
        with transaction.atomic():
            if isinstance(data, list):
                for item in data:
                    self.procesar_grupo(usuario, item)
            else:
                self.procesar_grupo(usuario, data)
            
            grupos = GrupoEngorda.objects.filter(
                usuario=usuario,
                eliminado=False
            )
            serializer = self.get_serializer(grupos, many=True)
            return Response(serializer.data)
    
    def procesar_grupo(self, usuario, data):
        id_local = data.get('id_local')
        
        if data.get('eliminado', False):
            GrupoEngorda.objects.filter(
                usuario=usuario,
                id_local=id_local
            ).update(eliminado=True, sincronizado=True)
            return
        
        defaults = {
            'origen': data.get('origen'),
            'cerda_id': data.get('cerda_id'),
            'ciclo_id': data.get('ciclo_id'),
            'cantidad': data.get('cantidad'),
            'raza': data.get('raza'),
            'peso_promedio': data.get('peso_promedio'),
            'corral_id': data.get('corral_id'),
            'etapa_alimento': data.get('etapa_alimento'),
            'proveedor': data.get('proveedor'),
            'fecha_compra': data.get('fecha_compra'),
            'fecha_ingreso': data.get('fecha_ingreso'),
            'activo': data.get('activo', True),
            'sincronizado': True,
            'eliminado': False
        }
        
        GrupoEngorda.objects.update_or_create(
            usuario=usuario,
            id_local=id_local,
            defaults=defaults
        )

# ----- Vistas para Eventos -----
class EventoCalendarioListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventoCalendarioSerializer
    
    def get_queryset(self):
        return EventoCalendario.objects.filter(
            usuario=self.request.user,
            eliminado=False
        )
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class EventoCalendarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventoCalendarioSerializer
    
    def get_queryset(self):
        return EventoCalendario.objects.filter(
            usuario=self.request.user
        )
    
    def perform_destroy(self, instance):
        instance.eliminado = True
        instance.sincronizado = False
        instance.save()

class SincronizarEventosView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventoCalendarioSerializer
    
    def post(self, request):
        usuario = request.user
        data = request.data
        
        with transaction.atomic():
            if isinstance(data, list):
                for item in data:
                    self.procesar_evento(usuario, item)
            else:
                self.procesar_evento(usuario, data)
            
            eventos = EventoCalendario.objects.filter(
                usuario=usuario,
                eliminado=False
            )
            serializer = self.get_serializer(eventos, many=True)
            return Response(serializer.data)
    
    def procesar_evento(self, usuario, data):
        id_local = data.get('id_local')
        
        if data.get('eliminado', False):
            EventoCalendario.objects.filter(
                usuario=usuario,
                id_local=id_local
            ).update(eliminado=True, sincronizado=True)
            return
        
        defaults = {
            'cerda_id': data.get('cerda_id'),
            'cerda_nombre': data.get('cerda_nombre'),
            'tipo_evento': data.get('tipo_evento'),
            'fecha': data.get('fecha'),
            'notas': data.get('notas'),
            'completado': data.get('completado', False),
            'sincronizado': True,
            'eliminado': False
        }
        
        EventoCalendario.objects.update_or_create(
            usuario=usuario,
            id_local=id_local,
            defaults=defaults
        )