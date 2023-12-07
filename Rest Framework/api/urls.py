from django.urls import path,include
from rest_framework import routers
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router=routers.DefaultRouter()
router.register(r'clients',views.ClienteViewSet)
router.register(r'employees',views.EmpleadoViewSet)
router.register(r'products',views.ProductoViewSet)
router.register(r'users',views.UsuariosViewSet)
router.register(r'facturacion',views.FacturaViewSet)
router.register(r'facDetalle',views.FacDetalleViewSet)
urlpatterns=[
    path('',include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get/no_fact/<int:num_factura>/', views.FacturaNumero, name='no_fact'),
    path('get/crsftoken/',views.get_custom_csrf_token,name='crsftoken'),
    path('create-checkout-session/<int:quantity>/<str:stripe_id>/<str:username>/', views.StripeCheckoutView.as_view()),
]