# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, inlineformset_factory

from cliente.models import Cliente, Recaudo, Recibido
from producto.models import Producto, ProductoBase

from .models import Gasto


class RecibidoForm(ModelForm):
    class Meta:
        model = Recibido
        fields = ['cliente', 'descuento', 'abono']
        exclude = ['saldo', 'subtotal']


class GastoForm(ModelForm):
    class Meta:
        model = Gasto
        fields = ['elemento_gasto', 'valor']


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = [
            'producto_base', 'cantidad', 'detalle', 'ancho', 'alto', 'total'
        ]


ProductoFormSet = inlineformset_factory(
    Recibido,
    Producto,
    form=ProductoForm,
    can_delete=False,
    extra=0,
    min_num=1,
    max_num=None)


class RecaudoForm(ModelForm):
    class Meta:
        model = Recaudo
        fields = ['recibido', 'valor']


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre_completo', 'tipo_identificacion', 'numero_identificacion'
        ]


class ProductoBaseForm(ModelForm):
    class Meta:
        model = ProductoBase
        fields = [
            'nombre', 'valor', 'valor_cantidad', 'factor', 'especificacion',
            'opciones_cobro'
        ]


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Opcional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Opcional.')
    email = forms.EmailField(
        max_length=254,
        help_text=
        'Requerido. Informar una dirección de correo electrónico válida.')

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password1',
            'password2'
        ]
