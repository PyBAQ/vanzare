# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible



@python_2_unicode_compatible
class ElementoGasto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Elementos de Gasto"
        verbose_name = "Elemento de Gasto"

    def __str__(self):
        return self.nombre


@python_2_unicode_compatible
class Gasto(models.Model):
    elemento_gasto = models.ForeignKey(ElementoGasto, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Gastos"
        verbose_name = "Gasto"

    def __str__(self):
        return str(self.valor)
