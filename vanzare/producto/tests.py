from django.test import TestCase
from .models import ProductoBase, Producto
# Create your tests here.


class ProductoBaseTestCase(TestCase):

    fixtures = ['cliente.test.json', 'producto.test.json']

    def test_producto_base_crear(self):
        ProductoBase.objects.create(
            nombre='Producto test',
            valor = 100,
            valor_cantidad = 1,
            opciones_cobro = ProductoBase.PRECIO_ESTANDAR
        )
        self.assertEqual(ProductoBase.objects.count(), 2)

    def test_producto_crear(self):
        Producto.objects.create(
            recibido_id=1,
            producto_base_id=1,
            cantidad=1,
        )
        self.assertEqual(Producto.objects.count(),2)
