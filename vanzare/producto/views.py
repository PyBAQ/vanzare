# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

import pdfkit
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from templated_docs import fill_template
from templated_docs.http import FileResponse

from facturacion.forms import (ClienteForm, GastoForm, ProductoBaseForm, ProductoFormSet, RecaudoForm, RecibidoForm,
                               RegistroForm)
from .models import Producto, ProductoBase

@login_required
def productosListar(request):
    productos = ProductoBase.objects.all().order_by('-id')
    context = {
        'productos': productos,
    }
    return render(request, 'facturacion/productos-base/listar.html', context)


@login_required
def productosCrear(request):
    titulo = "Productos"
    if request.method == 'POST':
        formulario = ProductoBaseForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse('productos-listar'))
    else:
        formulario = ProductoBaseForm()
    informacion = {
        'formulario': formulario,
        'titulo': titulo,
    }
    return render(request, "facturacion/parciales/crear.html", informacion)

@login_required
def productosEditar(request, pk):
    titulo = "Productos"
    producto = get_object_or_404(ProductoBase, pk=pk)
    if request.method == 'POST':
        formulario = ProductoBaseForm(request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse('productos-listar'))
    else:
        formulario = ProductoBaseForm(instance=producto)
    informacion = {
        'formulario': formulario,
        'titulo': titulo,
    }
    return render(request, "facturacion/parciales/crear.html", informacion)

