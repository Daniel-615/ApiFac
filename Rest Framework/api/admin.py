from django.contrib import admin
from .models import Cliente,Empleado,Producto,Usuarios,Facturacion,FacDetalle,UserPayment


from django.contrib.auth.models import Group

admin.site.unregister(Group)
@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  
    list_display_links = ('id',)   
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Producto)
admin.site.register(Usuarios)
admin.site.register(Facturacion)
admin.site.register(FacDetalle)
admin.site.register(UserPayment)