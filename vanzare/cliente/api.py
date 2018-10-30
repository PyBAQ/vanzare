from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from api.views import BasicViewSet

from .models import Cliente, Recaudo, Recibido
from .serializers import ClienteSerializer, RecaudoSerializer, RecibidoSerializer


class ClienteViewSet(BasicViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ('nombre_completo', 'numero_identificacion')


class RecaudoViewSet(BasicViewSet):
    queryset = Recaudo.objects.all()
    serializer_class = RecaudoSerializer

    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ('cliente__nombre_completo', 'cliente__numero_identificacion')


class RecibidoViewSet(BasicViewSet):
    queryset = Recibido.objects.all()
    serializer_class = RecibidoSerializer
