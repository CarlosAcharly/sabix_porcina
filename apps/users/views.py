# backend/apps/users/views.py
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import Usuario, ConfiguracionSistema
from .serializers import UsuarioSerializer, RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generar tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UsuarioSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'subscription': {
                'activa': True,
                'fecha_fin': user.fecha_fin_periodo_prueba,
                'dias_restantes': user.dias_restantes(),
                'en_periodo_prueba': True
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Verificar suscripción
        if not user.tiene_suscripcion_activa():
            return Response(
                {
                    'error': 'Suscripción inactiva',
                    'requires_payment': True,
                    'dias_restantes': user.dias_restantes()
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Generar tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UsuarioSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'subscription': {
                'activa': user.tiene_suscripcion_activa(),
                'fecha_fin': user.fecha_fin_periodo_prueba or user.fecha_fin_suscripcion,
                'dias_restantes': user.dias_restantes(),
                'en_periodo_prueba': user.periodo_prueba_activo
            }
        })

class VerificarSuscripcionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        activa = user.tiene_suscripcion_activa()
        
        fecha_fin = user.fecha_fin_periodo_prueba if user.periodo_prueba_activo else user.fecha_fin_suscripcion
        
        return Response({
            'activa': activa,
            'fecha_fin': fecha_fin,
            'dias_restantes': user.dias_restantes(),
            'en_periodo_prueba': user.periodo_prueba_activo
        })

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({"message": "Sesión cerrada exitosamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)