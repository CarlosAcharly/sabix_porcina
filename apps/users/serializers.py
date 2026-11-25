# backend/apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from .models import Usuario, ConfiguracionSistema

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 
                 'fecha_registro', 'suscripcion_activa', 'periodo_prueba_activo')
        read_only_fields = ('fecha_registro', 'suscripcion_activa', 'periodo_prueba_activo')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = Usuario
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        config = ConfiguracionSistema.get_config()
        
        user = Usuario(
            email=validated_data['email'],
            username=validated_data.get('username', validated_data['email']),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.periodo_prueba_activo = True
        user.fecha_fin_periodo_prueba = timezone.now() + timedelta(days=config.dias_prueba)
        user.save()
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(username=email, password=password)
        
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")
        
        if not user.is_active:
            raise serializers.ValidationError("Usuario desactivado")
        
        data['user'] = user
        return data