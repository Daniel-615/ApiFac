from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission   
from django.dispatch import receiver
from django.db.models.signals import post_save
class Cliente(models.Model):
    full_name=models.CharField(
        max_length=100,
        blank=False,
        verbose_name='name'
        )
    nit=models.CharField(
        max_length=20,
        blank=False
        )
    razon_social=models.CharField(
        max_length=30,
        verbose_name='razon',
        blank=False
        )
    direccion=models.CharField(
        max_length=50
        ,blank=False
        )
    telefono=models.CharField(
        max_length=10,
        blank=False
        )
    email=models.EmailField(
        max_length=20,
        blank=False,
        unique=True
        )
    fecha_ingreso=models.DateField(
        auto_now=True
        )
    status=models.BooleanField(
        default=True
        )
    
    

class Empleado(models.Model):
    full_name=models.CharField(
        max_length=30,
        blank=False,
        verbose_name='name'
        )
    nit=models.CharField(
        max_length=15,
        blank=False
    )
    salary=models.IntegerField(
        blank=False,
        null=False,
        help_text="Enter the salary"
    )
    status=models.BooleanField(
        default=True
    )
class Producto(models.Model):
    name=models.CharField(
        max_length=20,
        blank=False,
        null=False
    )
    description=models.CharField(
        max_length=100,
        blank=False,
        help_text="Give a description to a product",
        null=False
    )
    stripe_id=models.CharField(
        max_length=30,
    )
    stock=models.IntegerField(
    )
    stock_min=models.IntegerField(
    )
    unit_price=models.FloatField(
        blank=False,
        help_text='Give a price to a product'
    )
   

class Usuarios(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='usuarios_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='usuarios_permissions')

class UserPayment(models.Model):
    app_user=models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    payment_bool=models.BooleanField(default=False)
    stripe_checkout_id=models.CharField(max_length=500)
@receiver(post_save,sender=Usuarios)
def create_user_payment(sender,instance,created,**kwargs):
    if created:
        UserPayment.objects.create(Usuarios=instance)


class Facturacion(models.Model):
    no_factura=models.IntegerField(
        blank=False,
        null=True
    )
    serie=models.CharField(
        max_length=1,
        blank=False,
        default='A'
    )
    id_client=models.ForeignKey(
        Cliente,        
        on_delete=models.CASCADE,  
        related_name='Clients',   
        verbose_name='Client',     
    )
    id_employee=models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='Employees',
        verbose_name='Employee'
    )
    
class FacDetalle(models.Model):
    id_factura=models.ForeignKey(
        Facturacion,
        on_delete=models.CASCADE,
        related_name='Facturacion',
        verbose_name='Factura'
    )
    id_product=models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='Products',
        verbose_name='Product'
    )
    quantity=models.IntegerField(
        blank=False
    )
    sell_price=models.FloatField(
        blank=False,
        help_text='Enter the price'
    )
