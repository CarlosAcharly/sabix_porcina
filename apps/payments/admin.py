# backend/apps/payments/admin.py
from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('referencia_pago', 'usuario', 'monto', 'status', 'fecha_pago')
    list_filter = ('status', 'metodo_pago', 'fecha_pago')
    search_fields = ('referencia_pago', 'usuario__email')
    readonly_fields = ('fecha_pago', 'fecha_confirmacion')
    ordering = ('-fecha_pago',)