from django.contrib import admin

# Register your models here.
from .models import Cliente, Recaudo


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'tipo_identificacion', 'numero_identificacion')


admin.site.register(Cliente, ClienteAdmin)


class RecaudoAdmin(admin.ModelAdmin):
    list_display = ('recibido', 'valor', 'fecha')


admin.site.register(Recaudo, RecaudoAdmin)
