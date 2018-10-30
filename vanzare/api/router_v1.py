from rest_framework import routers
from .views import UserViewSet, GroupViewSet
from cliente.api import ClienteViewSet, RecaudoViewSet, RecibidoViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'recaudos', RecaudoViewSet)
router.register(r'recibidos', RecibidoViewSet)
