# backend/apps/sync/serializers.py
from rest_framework import serializers
from .models import Cerda, GrupoEngorda, EventoCalendario

class CerdaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cerda
        fields = '__all__'
        read_only_fields = ('usuario', 'fecha_registro', 'fecha_actualizacion')

class GrupoEngordaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoEngorda
        fields = '__all__'
        read_only_fields = ('usuario', 'fecha_registro', 'fecha_actualizacion')

class EventoCalendarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoCalendario
        fields = '__all__'
        read_only_fields = ('usuario', 'fecha_registro', 'fecha_actualizacion')