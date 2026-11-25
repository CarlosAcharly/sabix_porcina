# backend/apps/sync/admin.py
from django.contrib import admin
from .models import Cerda, GrupoEngorda, EventoCalendario

@admin.register(Cerda)
class CerdaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'arete', 'estado', 'usuario', 'sincronizado')
    list_filter = ('estado', 'sincronizado', 'eliminado')
    search_fields = ('nombre', 'arete', 'usuario__email')
    ordering = ('-fecha_registro',)

@admin.register(GrupoEngorda)
class GrupoEngordaAdmin(admin.ModelAdmin):
    list_display = ('id', 'origen', 'cantidad', 'raza', 'activo', 'sincronizado')
    list_filter = ('origen', 'activo', 'sincronizado', 'eliminado')
    search_fields = ('raza', 'proveedor', 'usuario__email')
    ordering = ('-fecha_ingreso',)

@admin.register(EventoCalendario)
class EventoCalendarioAdmin(admin.ModelAdmin):
    list_display = ('tipo_evento', 'cerda_nombre', 'fecha', 'completado', 'usuario')
    list_filter = ('tipo_evento', 'completado', 'sincronizado', 'eliminado')
    search_fields = ('cerda_nombre', 'cerda_id', 'usuario__email')
    ordering = ('-fecha',)