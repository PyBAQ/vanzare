from rest_framework import serializers

from .models import Cliente, Recibido, Recaudo


class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = ('__all__')


class RecibidoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recibido
        fields = ('__all__')


class RecaudoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recaudo
        fields = ('__all__')
