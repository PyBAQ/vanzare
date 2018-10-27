# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pdfkit
from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from facturacion.forms import (RecibidoForm, GastoForm, ProductoFormSet,
                               RecaudoForm, ClienteForm, ProductoBaseForm,
                               RegistroForm)
from facturacion.models import Gasto, Producto, ProductoBase
from cliente.models import Recibido, Cliente, Recaudo
today = date.today()


@login_required
def index(request):
    recibidos = Recibido.objects.all().filter(fecha__date=today)
    gastos = Gasto.objects.all().filter(fecha__date=today)
    total_recibidos = recibidos.aggregate(suma=Sum('saldo'))
    total_gastos = gastos.aggregate(suma=Sum('valor'))
    context = {
        'recibidos': recibidos,
        'gastos': gastos,
        'total_recibidos': total_recibidos['suma'],
        'total_gastos': total_gastos['suma'],
    }
    return render(request, 'facturacion/index.html', context)


@login_required
def recibidosFacturar(request):
    productos = ProductoBase.objects.all()
    if request.method == 'POST':
        formulario = RecibidoForm(request.POST)
        subtotal = 0
        if formulario.is_valid():
            formulario_guardado = formulario.save(commit=False)
            producto_formset = ProductoFormSet(
                request.POST, instance=formulario_guardado)

            if producto_formset.is_valid():
                for form in producto_formset:
                    # Se tiene en cuenta si la opcion de cobro es estandar/por_docena o personalizado
                    if form.cleaned_data[
                            'producto_base'].opciones_cobro == 'estandar' or form.cleaned_data[
                                'producto_base'].opciones_cobro == 'por_docena':
                        if form.cleaned_data[
                                'producto_base'].valor_cantidad and form.cleaned_data[
                                    'cantidad'] != 1:
                            subtotal += form.cleaned_data[
                                'producto_base'].valor_cantidad * form.cleaned_data[
                                    'cantidad']
                        else:
                            subtotal += form.cleaned_data[
                                'producto_base'].valor * form.cleaned_data[
                                    'cantidad']
                    elif form.cleaned_data[
                            'producto_base'].opciones_cobro == 'personalizado':
                        subtotal += form.cleaned_data[
                            'producto_base'].factor * form.cleaned_data[
                                'cantidad'] * form.cleaned_data[
                                    'ancho'] * form.cleaned_data['alto']

                formulario_guardado.subtotal = subtotal
                formulario_guardado.saldo = subtotal - formulario_guardado.abono

                if formulario_guardado.abono != formulario_guardado.subtotal:
                    formulario_guardado.total = formulario_guardado.saldo - (
                        subtotal * formulario_guardado.descuento / 100)
                else:
                    formulario_guardado.total = formulario_guardado.subtotal

                formulario_guardado.save()
                producto_comprado = producto_formset.save()
                recibido = Recibido.objects.get(pk=formulario_guardado.id)

                if recibido.saldo == 0:
                    recibido.recaudado = True
                    recibido.save()

                for producto in producto_comprado:
                    # Se tiene en cuenta las opciones de cobro y si existe valor_cantidad
                    if producto.producto_base.opciones_cobro == 'estandar' or producto.producto_base.opciones_cobro == 'por_docena':
                        if producto.producto_base.valor_cantidad and producto.cantidad != 1:
                            producto.total = producto.producto_base.valor_cantidad * producto.cantidad
                        else:
                            producto.total = producto.producto_base.valor * producto.cantidad
                    elif producto.producto_base.opciones_cobro == 'personalizado':
                        producto.total = producto.producto_base.factor * producto.cantidad * producto.ancho * producto.alto
                    producto.save()
                return HttpResponseRedirect(reverse('recibidos-listar'))
    else:
        formulario = RecibidoForm()
        producto_formset = ProductoFormSet()
    informacion = {
        'formulario': formulario,
        'formset': producto_formset,
        'productos': productos,
    }
    return render(request, "facturacion/recibidos/facturar.html", informacion)


@login_required
def gastos(request):
    titulo = "Gastos"
    if request.method == 'POST':
        formulario = GastoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = GastoForm()
    informacion = {
        'formulario': formulario,
        'titulo': titulo,
    }
    return render(request, "facturacion/parciales/crear.html", informacion)


@login_required
def recibidosListar(request):
    recibidos = Recibido.objects.all().order_by('-id')
    total_recibidos = recibidos.aggregate(suma=Sum('saldo'))
    context = {
        'recibidos': recibidos,
        'total_recibidos': total_recibidos['suma'],
        'hoy': today,
    }
    return render(request, 'facturacion/recibidos/listar.html', context)


@login_required
def imprimirFactura(request, pk):

    domain = request.META['HTTP_HOST']
    url = 'http://' + domain + '/factura/' + pk

    pdf = pdfkit.from_url(url, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response[
        'Content-Disposition'] = 'attachment; filename="factura_' + pk + '.pdf"'
    return response


@login_required
def factura(request, pk):
    recibido = Recibido.objects.get(pk=pk)
    productos = Producto.objects.filter(recibido=recibido)
    identificador_recibido = recibido.id
    factura = {
        'cliente': str(recibido.cliente),
        'tipo_id': str(recibido.cliente.tipo_identificacion),
        'id_cliente': str(recibido.cliente.numero_identificacion),
        'abono': str(recibido.abono),
        'subtotal': str(recibido.subtotal),
        'total': str(recibido.total),
        'descuento': str(recibido.descuento),
        'saldo': str(recibido.saldo),
        'anio': recibido.fecha.date().year,
        'dia': recibido.fecha.date().day,
        'mes': recibido.fecha.date().month,
        'productos': productos,
        'identificador': identificador_recibido,
    }
    return render(request, "facturacion/impresos/factura.html", factura)


@login_required
def escogerCierre(request):
    return render(request, "facturacion/escoger/cierre.html")


@login_required
def cierreDia(request, day, month, year):
    recibidos = Recibido.objects.filter(
        fecha__year=year, fecha__month=month, fecha__day=day)
    recaudos = Recaudo.objects.filter(
        fecha__year=year, fecha__month=month, fecha__day=day)
    gastos = Gasto.objects.all().filter(
        fecha__year=year, fecha__month=month, fecha__day=day)
    context = {
        'recibidos': recibidos,
        'mes': month,
        'anio': year,
        'dia': day,
        'recaudos': recaudos,
        'gastos': gastos,
    }
    return render(request, "facturacion/cierres/dia.html", context)


@login_required
def cierreMes(request, month, year):
    recibidos = Recibido.objects.filter(fecha__year=year, fecha__month=month)
    gastos = Gasto.objects.filter(fecha__year=year, fecha__month=month)
    total_recibidos = recibidos.aggregate(suma=Sum('total'))
    total_gastos = gastos.aggregate(suma=Sum('valor'))
    context = {
        'recibidos': recibidos,
        'gastos': gastos,
        'mes': month,
        'anio': year,
        'total_recibidos': total_recibidos['suma'],
        'total_gastos': total_gastos['suma'],
    }
    return render(request, "facturacion/cierres/mes.html", context)


@login_required
def verImpresoCierreMes(request, month, year):
    recibidos = Recibido.objects.filter(fecha__year=year, fecha__month=month)
    gastos = Gasto.objects.filter(fecha__year=year, fecha__month=month)
    recibos_de_caja = recibidos.aggregate(suma=Sum('total'))
    total_gastos = gastos.aggregate(suma=Sum('valor'))

    cierre_mes = {
        'anio': year,
        'mes': month,
        'recibidos': recibidos,
        'total_gastos': total_gastos['suma'],
        'recibos_de_caja': recibos_de_caja['suma'],
    }
    return render(request, "facturacion/impresos/cierre-mes.html", cierre_mes)


@login_required
def imprimirCierreMes(request, month, year):
    domain = request.META['HTTP_HOST']
    url = 'http://' + domain + '/ver-impreso-cierre-mes/' + month + '/' + year + '/'

    pdf = pdfkit.from_url(url, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response[
        'Content-Disposition'] = 'attachment; filename="cierre_mes' + month + '.pdf"'
    return response


@login_required
def imprimirCierreDia(request, day, month, year):
    domain = request.META['HTTP_HOST']
    url = 'http://' + domain + '/ver-impreso-cierre-dia/' + day + '/' + month + '/' + year + '/'

    pdf = pdfkit.from_url(url, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"cierre_' + {day} + '_' + {month} + '_' + {year} + '.pdf"
    response['Content-Disposition'] = 'attachment; filename=""'.format(
        filename)
    return response


@login_required
def verImpresoCierreDia(request, day, month, year):
    recibidos = Recibido.objects.filter(
        fecha__year=year, fecha__month=month, fecha__day=day)
    recaudos = Recaudo.objects.filter(
        fecha__year=year, fecha__month=month, fecha__day=day)
    gastos = Gasto.objects.all().filter(
        fecha__year=year, fecha__month=month, fecha__day=day)
    total_recibidos = recibidos.aggregate(suma=Sum('subtotal'))
    total_recaudos = recaudos.aggregate(suma=Sum('valor'))
    total_efectivo = total_recibidos['suma'] + total_recaudos['suma']
    total_gastos = gastos.aggregate(suma=Sum('valor'))
    saldo_efectivo = total_efectivo - total_gastos['suma']
    cierre_dia = {
        'recibidos': recibidos,
        'mes': month,
        'anio': year,
        'dia': day,
        'recaudos': recaudos,
        'total_efectivo': total_efectivo,
        'gastos': gastos,
        'total_gastos': total_gastos['suma'],
        'saldo_efectivo': saldo_efectivo,
    }
    return render(request, "facturacion/impresos/cierre-dia.html", cierre_dia)


@login_required
def escogerRecaudo(request):
    if request.method == 'POST':
        formulario = RecaudoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/')
    else:
        formulario = RecaudoForm()
    informacion = {
        'formulario': formulario,
    }
    return render(request, "facturacion/escoger/recaudo.html", informacion)


@login_required
def recaudo(request, pk):
    recibido = get_object_or_404(Recibido, pk=pk)
    if request.method == 'POST':
        formulario = RecaudoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse('recaudos-listar'))
    else:
        formulario = RecaudoForm(initial={
            'valor': recibido.saldo,
            'recibido': recibido.pk
        })
    informacion = {
        'formulario': formulario,
        'recibido': recibido,
    }
    return render(request, "facturacion/recaudos/recaudo.html", informacion)


@login_required
def verImpresoRecaudo(request, pk):
    recaudo = get_object_or_404(Recaudo, pk=pk)
    productos = Producto.objects.filter(recibido=recaudo.recibido)
    informacion = {
        'recaudo': recaudo,
        'productos': productos,
    }
    return render(request, "facturacion/impresos/recaudo.html", informacion)


@login_required
def imprimirRecaudo(request, pk):
    domain = request.META['HTTP_HOST']
    url = 'http://' + domain + '/ver-impreso-recaudo/' + pk + '/'

    pdf = pdfkit.from_url(url, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response[
        'Content-Disposition'] = 'attachment; filename="recaudo_' + pk + '_' + '.pdf"'
    return response


@login_required
def recaudosListar(request):
    recaudos = Recaudo.objects.all().order_by('-id')
    context = {
        'recaudos': recaudos,
    }
    return render(request, 'facturacion/recaudos/listar.html', context)


@login_required
def clientesListar(request):
    clientes = Cliente.objects.all().order_by('-id')
    context = {
        'clientes': clientes,
    }
    return render(request, 'facturacion/clientes/listar.html', context)


@login_required
def productosListar(request):
    productos = ProductoBase.objects.all().order_by('-id')
    context = {
        'productos': productos,
    }
    return render(request, 'facturacion/productos-base/listar.html', context)


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
            # username = formulario.cleaned_data.get('username')
            # raw_password = formulario.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
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
