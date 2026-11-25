# backend/apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, ConfiguracionSistema

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 
                   'suscripcion_activa', 'periodo_prueba_activo', 'dias_restantes')
    list_filter = ('suscripcion_activa', 'periodo_prueba_activo', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Suscripción', {
            'fields': (
                'suscripcion_activa',
                'fecha_inicio_suscripcion',
                'fecha_fin_suscripcion',
                'periodo_prueba_activo',
                'fecha_fin_periodo_prueba'
            ),
        }),
    )
    
    def dias_restantes(self, obj):
        return obj.dias_restantes()
    dias_restantes.short_description = 'Días restantes'

@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ('precio_mensual', 'dias_prueba', 'moneda')
    fieldsets = (
        ('Configuración de Pagos', {
            'fields': ('precio_mensual', 'moneda', 'grace_period_dias')
        }),
        ('Configuración de Prueba', {
            'fields': ('dias_prueba',)
        }),
        ('Stripe', {
            'fields': ('stripe_public_key', 'stripe_secret_key'),
            'classes': ('collapse',)
        }),
    )