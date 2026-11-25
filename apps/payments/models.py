# backend/apps/payments/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Pago(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
    )
    
    METODOS = (
        ('stripe', 'Stripe'),
        ('mercadopago', 'MercadoPago'),
        ('conekta', 'Conekta'),
        ('manual', 'Manual'),
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='pagos'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    fecha_inicio_suscripcion = models.DateTimeField()
    fecha_fin_suscripcion = models.DateTimeField()
    metodo_pago = models.CharField(max_length=50, choices=METODOS)
    referencia_pago = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    metadata = models.JSONField(default=dict, blank=True)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Pago {self.referencia_pago} - {self.usuario.email}"
    
    def confirmar_pago(self):
        self.status = 'completado'
        self.fecha_confirmacion = timezone.now()
        self.save()
        usuario = self.usuario
        usuario.suscripcion_activa = True
        usuario.fecha_inicio_suscripcion = self.fecha_inicio_suscripcion
        usuario.fecha_fin_suscripcion = self.fecha_fin_suscripcion
        usuario.periodo_prueba_activo = False
        usuario.save()