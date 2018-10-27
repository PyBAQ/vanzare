from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^recibidos/listar', views.recibidosListar, name='recibidos-listar'),
    url(r'^recibidos/facturar', views.recibidosFacturar, name='recibidos-facturar'),
    url(r'^gastos/', views.gastos, name='gastos'),
    url(r'^factura/(?P<pk>\d+)/', views.factura, name='factura'),
    url(r'^print/(?P<pk>\d+)/', views.imprimirFactura, name='print'),
    url(r'^imprimir-cierre-mes/(?P<month>\d{2})/(?P<year>\d{4})/', views.imprimirCierreMes, name='imprimir-cierre-mes'),
    url(r'^ver-impreso-cierre-mes/(?P<month>\d{2})/(?P<year>\d{4})/', views.verImpresoCierreMes, name='ver-impreso-cierre-mes'),
    url(r'^imprimir-cierre-dia/(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/', views.imprimirCierreDia, name='imprimir-cierre-dia'),
    url(r'^ver-impreso-cierre-dia/(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})/', views.verImpresoCierreDia, name='ver-impreso-cierre-dia'),
    url(r'^escoger-cierre', views.escogerCierre, name='escoger-cierre'),
    url(r'^cierre-dia-(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', views.cierreDia, name='cierre-dia'),
    url(r'^cierres-mes/(?P<month>\d{2})/(?P<year>\d{4})/', views.cierreMes, name='cierre-mes'),
    url(r'^recaudo/(?P<pk>\d+)/', views.recaudo, name='recaudo'),
    url(r'^imprimir-recaudo/(?P<pk>\d+)/', views.imprimirRecaudo, name='imprimir-recaudo'),
    url(r'^ver-impreso-recaudo/(?P<pk>\d+)/', views.verImpresoRecaudo, name='ver-impreso-recaudo'),
    url(r'^escoger-recaudo', views.escogerRecaudo, name='escoger-recaudo'),
    url(r'^recaudos/listar/$', views.recaudosListar, name='recaudos-listar'),

    url(r'^productos/listar/$', views.productosListar, name='productos-listar'),
    url(r'^productos/crear/$', views.productosCrear, name='productos-crear'),
    url(r'^productos/editar/(?P<pk>[0-9]+)/$', views.productosEditar, name='productos-editar'),
    url(r'^troregis/$', views.registroUsuario, name='registro'),
]
