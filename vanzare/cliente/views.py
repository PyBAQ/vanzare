# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from facturacion.forms import ClienteForm, RegistroForm

from .models import Cliente

today = date.today()


@login_required
def clientesListar(request):
    clientes = Cliente.objects.all().order_by('-id')
    context = {
        'clientes': clientes,
    }
    return render(request, 'facturacion/clientes/listar.html', context)


@login_required
def clientesCrear(request):
    titulo = "Clientes"
    if request.method == 'POST':
        formulario = ClienteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse('clientes-listar'))
    else:
        formulario = ClienteForm()
    informacion = {
        'formulario': formulario,
        'titulo': titulo,
    }
    return render(request, "facturacion/parciales/crear.html", informacion)


@login_required
def clientesEditar(request, pk):
    titulo = "Clientes"
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        formulario = ClienteForm(request.POST, instance=cliente)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse('clientes-listar'))
    else:
        formulario = ClienteForm(instance=cliente)
    informacion = {
        'formulario': formulario,
        'titulo': titulo,
    }
    return render(request, "facturacion/parciales/crear.html", informacion)


def registroUsuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            usuario.is_active = False
            usuario.save()
            return redirect('index')
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))
        else:
            formulario = RegistroForm()
    informacion = {
        'formulario': formulario,
    }
    return render(request, 'registration/registro.html', informacion)
