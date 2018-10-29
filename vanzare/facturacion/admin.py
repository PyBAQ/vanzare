# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ElementoGasto, Gasto
from producto.models import Producto
from cliente.models import Recibido


class ProductoInLine(admin.StackedInline):
    model = Producto
    extra = 0


class ElementoGastoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha', 'modificado')


admin.site.register(ElementoGasto, ElementoGastoAdmin)


class GastoAdmin(admin.ModelAdmin):
    list_display = ('elemento_gasto', 'valor', 'fecha', 'modificado')


admin.site.register(Gasto, GastoAdmin)


class RecibidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'id', 'fecha', 'descuento', 'abono', 'saldo', 'total', 'recaudado')
    inlines = [ProductoInLine]


admin.site.register(Recibido, RecibidoAdmin)
