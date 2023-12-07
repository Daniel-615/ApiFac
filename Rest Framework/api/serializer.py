from rest_framework import serializers
from .models import Cliente,Empleado,Producto,Usuarios,Facturacion,FacDetalle

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cliente
        fields='__all__'
class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Empleado
        fields='__all__'
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Producto
        fields='__all__'
class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model=Usuarios
        fields='__all__'
class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Facturacion
        fields='__all__'
class FacDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model=FacDetalle
        fields='__all__'