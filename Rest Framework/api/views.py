from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
import stripe
from django.shortcuts import redirect
from .serializer import (
    ClienteSerializer,
    FacturaSerializer,
    EmpleadoSerializer,
    ProductoSerializer,
    UsuariosSerializer,
    FacDetalleSerializer,
)
from .models import (
    Cliente,
    Empleado,
    Producto,
    Usuarios,
    Facturacion,
    FacDetalle,
    UserPayment
)
from rest_framework.decorators import api_view

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Facturacion.objects.all()
    serializer_class = FacturaSerializer

@api_view(['GET'])
def FacturaNumero(request, num_factura):
    try:
        factura = Facturacion.objects.get(no_factura=num_factura)
        serializer = FacturaSerializer(factura)
        return Response(serializer.data)
    except Facturacion.DoesNotExist:
        return Response({"message": "Factura no encontrada"}, status=404)
    except Facturacion.MultipleObjectsReturned:
        return Response({"message": "Múltiples facturas encontradas"}, status=400)

class FacDetalleViewSet(viewsets.ModelViewSet):
    queryset = FacDetalle.objects.all()
    serializer_class = FacDetalleSerializer


def get_custom_csrf_token(request):
    custom_csrf_token = get_token(request)  
    return JsonResponse({'csrf_token': custom_csrf_token})

stripe.api_key=settings.STRIPE_SECRET_KEY
class StripeCheckoutView(APIView):
    def post(self,request,quantity,stripe_id,username):
        try:
            user=Usuarios.objects.get(username=username)
            if not stripe_id or not quantity:
                return Response(
                    {'error': 'price_id and quantity are required parameters'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            checkout_session=stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': stripe_id,
                        'quantity':quantity,   
                    },
                ],
                payment_method_types=[
                    'card',
                ],
                mode='payment',
                success_url=settings.SITE_URL+'/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL+'/?canceled=true',
                
            )
            payment=UserPayment(app_user=user,payment_bool=True,stripe_checkout_id=checkout_session.id)
            payment.save()
            return redirect(checkout_session.url)
        except Exception as e:
            return Response(
                {'error':'Something went wrong when creating stripe checkout session '+str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )