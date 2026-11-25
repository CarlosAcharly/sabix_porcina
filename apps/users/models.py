# backend/apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_ultima_verificacion = models.DateTimeField(auto_now=True)
    suscripcion_activa = models.BooleanField(default=True)
    fecha_inicio_suscripcion = models.DateTimeField(null=True, blank=True)
    fecha_fin_suscripcion = models.DateTimeField(null=True, blank=True)
    periodo_prueba_activo = models.BooleanField(default=True)
    # Cambiar a null=True y blank=True para permitir valores nulos
    fecha_fin_periodo_prueba = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Si no tiene fecha_fin_periodo_prueba, establecer una fecha por defecto
        if not self.fecha_fin_periodo_prueba:
            self.fecha_fin_periodo_prueba = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)
    
    def tiene_suscripcion_activa(self):
        ahora = timezone.now()
        if self.periodo_prueba_activo and self.fecha_fin_periodo_prueba and self.fecha_fin_periodo_prueba > ahora:
            return True
        if self.suscripcion_activa and self.fecha_fin_suscripcion and self.fecha_fin_suscripcion > ahora:
            return True
        return False
    
    def dias_restantes(self):
        ahora = timezone.now()
        if self.periodo_prueba_activo and self.fecha_fin_periodo_prueba:
            return max(0, (self.fecha_fin_periodo_prueba - ahora).days)
        if self.fecha_fin_suscripcion:
            return max(0, (self.fecha_fin_suscripcion - ahora).days)
        return 0

class ConfiguracionSistema(models.Model):
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=30.00)
    dias_prueba = models.IntegerField(default=30)
    grace_period_dias = models.IntegerField(default=3)
    moneda = models.CharField(max_length=3, default='MXN')
    stripe_public_key = models.CharField(max_length=255, blank=True)
    stripe_secret_key = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name_plural = "Configuraciones del Sistema"
    
    def __str__(self):
        return f"Configuración (Precio: ${self.precio_mensual})"
    
    @classmethod
    def get_config(cls):
        config, created = cls.objects.get_or_create(id=1)
        return config