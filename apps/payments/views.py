# backend/apps/payments/views.py
import stripe
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from apps.users.models import ConfiguracionSistema
from .models import Pago
from .serializers import PagoSerializer, CrearPagoSerializer

class CrearIntentoPagoView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CrearPagoSerializer
    
    def post(self, request):
        # Verificar que Stripe está configurado
        if not settings.STRIPE_SECRET_KEY:
            return Response(
                {'error': 'El sistema de pagos no está configurado'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        config = ConfiguracionSistema.get_config()
        usuario = request.user
        
        if usuario.tiene_suscripcion_activa():
            return Response(
                {'error': 'Ya tienes una suscripción activa'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(float(config.precio_mensual) * 100),
                currency=config.moneda.lower(),
                metadata={
                    'user_id': usuario.id,
                    'user_email': usuario.email,
                    'suscripcion': 'mensual'
                },
                description=f"Suscripción mensual - {usuario.email}"
            )
            
            fecha_inicio = timezone.now()
            fecha_fin = fecha_inicio + timedelta(days=30)
            
            pago = Pago.objects.create(
                usuario=usuario,
                monto=config.precio_mensual,
                fecha_inicio_suscripcion=fecha_inicio,
                fecha_fin_suscripcion=fecha_fin,
                metodo_pago=serializer.validated_data.get('metodo_pago', 'stripe'),
                referencia_pago=intent.id,
                status='pendiente',
                metadata={
                    'payment_intent': intent.id,
                    'client_secret': intent.client_secret
                }
            )
            
            return Response({
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'public_key': settings.STRIPE_PUBLIC_KEY,
                'pago_id': pago.id,
                'monto': config.precio_mensual,
                'moneda': config.moneda
            })
            
        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class StripeWebhookView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        if not settings.STRIPE_WEBHOOK_SECRET:
            return Response(
                {'error': 'Webhook no configurado'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if event['type'] == 'payment_intent.succeeded':
            self.handle_successful_payment(event['data']['object'])
        elif event['type'] == 'payment_intent.payment_failed':
            self.handle_failed_payment(event['data']['object'])
        
        return Response(status=status.HTTP_200_OK)
    
    def handle_successful_payment(self, payment_intent):
        try:
            pago = Pago.objects.get(referencia_pago=payment_intent['id'])
            pago.confirmar_pago()
            print(f"✅ Pago confirmado: {pago.referencia_pago} - {pago.usuario.email}")
        except Pago.DoesNotExist:
            print(f"⚠️ Pago no encontrado: {payment_intent['id']}")
    
    def handle_failed_payment(self, payment_intent):
        try:
            pago = Pago.objects.get(referencia_pago=payment_intent['id'])
            pago.status = 'fallido'
            pago.save()
            print(f"❌ Pago fallido: {pago.referencia_pago} - {pago.usuario.email}")
        except Pago.DoesNotExist:
            print(f"⚠️ Pago no encontrado: {payment_intent['id']}")

class HistorialPagosView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PagoSerializer
    
    def get_queryset(self):
        return Pago.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha_pago')