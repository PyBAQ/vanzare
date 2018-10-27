# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@python_2_unicode_compatible
class Cliente(models.Model):
    CEDULA = 'cedula'
    NIT = 'nit'
    TIPO_DE_IDENTIFICACION = (
        (CEDULA, 'Cédula'),
        (NIT, 'NIT'),
    )
    nombre_completo = models.CharField(max_length=200)
    tipo_identificacion = models.CharField(
        max_length=15,
        choices=TIPO_DE_IDENTIFICACION,
        default=CEDULA,
    )
    numero_identificacion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True, blank=True, null = True)

    class Meta:
        verbose_name_plural = "Clientes"
        verbose_name = "Cliente"

    def __str__(self):
        return self.nombre_completo


@python_2_unicode_compatible
class Recibido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descuento = models.IntegerField(default=0)
    abono = models.IntegerField(default=0)
    saldo = models.IntegerField(default=0)
    subtotal = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True, blank=True, null = True)
    recaudado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Recibidos"
        verbose_name = "Recibido"

    def __str__(self):
        return str(self.pk)


@python_2_unicode_compatible
class ElementoGasto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True, blank=True, null = True)

    class Meta:
        verbose_name_plural = "Elementos de Gasto"
        verbose_name = "Elemento de Gasto"

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Gasto(models.Model):
    elemento_gasto =  models.ForeignKey(ElementoGasto, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True, blank=True, null = True)

    class Meta:
        verbose_name_plural = "Gastos"
        verbose_name = "Gasto"

    def __str__(self):
        return str(self.valor)


class Recaudo(models.Model):
    recibido = models.ForeignKey(Recibido, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Recaudos"
        verbose_name = "Recaudo"

    def __str__(self):
        return str(self.pk)


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField(max_length=500, blank=True)
    ubicacion = models.CharField(max_length=30, blank=True)
    fecha_de_nacimiento = models.DateField(null=True, blank=True)
    confirmar_email = models.BooleanField(default=False)

    def __str__(self):
        return str(self.usuario)

@receiver(post_save, sender=User)
def actualizar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)
    instance.perfil.save()
