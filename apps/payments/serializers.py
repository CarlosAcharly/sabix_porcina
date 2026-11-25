# backend/apps/payments/serializers.py
from rest_framework import serializers
from .models import Pago

class PagoSerializer(serializers.ModelSerializer):
    usuario_email = serializers.EmailField(source='usuario.email', read_only=True)
    
    class Meta:
        model = Pago
        fields = ('id', 'usuario', 'usuario_email', 'monto', 'fecha_pago', 
                 'fecha_inicio_suscripcion', 'fecha_fin_suscripcion', 
                 'metodo_pago', 'referencia_pago', 'status', 'fecha_confirmacion')
        read_only_fields = ('usuario', 'fecha_pago', 'status', 'fecha_confirmacion')

class CrearPagoSerializer(serializers.Serializer):
    metodo_pago = serializers.ChoiceField(choices=Pago.METODOS, default='stripe')