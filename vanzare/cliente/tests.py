from django.test import TestCase

from .models import Cliente, Recibido, Recaudo, Perfil



class ClienteTestCase(TestCase):
    fixtures = ['cliente.test.json']

    def test_cliente_crear(self):
        Cliente.objects.create(
            nombre_completo='Cliente Test 1',
            numero_identificacion='12121212'
        )

        self.assertEqual(Cliente.objects.count(), 2)



class RecibidoTestCase(TestCase):
    fixtures = ['cliente.test.json']

    def test_recibido_crear(self):
        Recibido.objects.create(
            cliente_id = 1,
        )
        self.assertEqual(Recibido.objects.count(), 2)


class RecaudoTestCase(TestCase):
    fixtures = ['cliente.test.json']

    def test_recaudo_crear(self):
        recibido = Recibido.objects.create(
            cliente_id = 1,
        )

        Recaudo.objects.create(
            recibido=recibido,
            valor=100
        )
        self.assertEqual(Recaudo.objects.count(), 1)


class PerfilTestCase(TestCase):
    fixtures = ['cliente.test.json']

    def test_perfil_crear(self):
        Cliente.objects.create(
            nombre_completo='Cliente Test 1',
            numero_identificacion='12121212'
        )
        self.assertEqual(Perfil.objects.count(), 1)

