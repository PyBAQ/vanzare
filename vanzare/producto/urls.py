from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^productos/listar/$', views.productosListar, name='productos-listar'),
    url(r'^productos/crear/$', views.productosCrear, name='productos-crear'),
    url(r'^productos/editar/(?P<pk>[0-9]+)/$', views.productosEditar, name='productos-editar'),
]
