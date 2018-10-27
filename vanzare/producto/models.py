from django.db import models
from facturacion.models import Recibido


class ProductoBase(models.Model):
    PRECIO_ESTANDAR = 'estandar'
    PERSONALIZADO = 'personalizado'
    POR_DOCENA = 'por_docena'
    FORMATO = (
        (PRECIO_ESTANDAR, 'Precio estándar'),
        (PERSONALIZADO, 'Personalizado'),
        (POR_DOCENA, 'Por docena'),
    )
    nombre = models.CharField(max_length=200)
    valor = models.PositiveIntegerField(help_text="Este será el valor unitario o el valor por docena, dependiendo del caso", blank=True, null=True)
    valor_cantidad = models.PositiveIntegerField(blank=True, null=True)
    factor = models.DecimalField(blank=True, null=True, max_digits=2, decimal_places=1)
    especificacion = models.CharField(max_length=255, blank=True, null=True, verbose_name='Especificación')
    fecha = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True, blank=True, null=True)
    opciones_cobro = models.CharField(
        max_length=100,
        choices=FORMATO,
    )

    class Meta:
        verbose_name_plural = "Productos Base"
        verbose_name = "Producto Base"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    recibido = models.ForeignKey(Recibido, on_delete=models.CASCADE)
    producto_base = models.ForeignKey(ProductoBase, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    detalle = models.CharField(max_length=200, default="", blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0, blank=True, null=True)
    ancho = models.PositiveIntegerField(blank=True, null=True, help_text="Los valores deben estar en centímetros")
    alto = models.PositiveIntegerField(blank=True, null=True, help_text="Los valores deben estar en centímetros")

    class Meta:
        verbose_name_plural = "Productos"
        verbose_name = "Producto"

    def __str__(self):
        return self.detalle
