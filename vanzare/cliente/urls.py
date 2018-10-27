from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^clientes/listar/$', views.clientesListar, name='clientes-listar'),
    url(r'^clientes/crear/$', views.clientesCrear, name='clientes-crear'),
    url(r'^clientes/editar/(?P<pk>[0-9]+)/$', views.clientesEditar, name='clientes-editar'),
]
