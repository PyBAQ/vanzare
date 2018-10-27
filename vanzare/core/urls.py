"""Documentation

Check the Mozilla Documentation about authenticacion
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication

Or the Simple Is Better Than Complex post
https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html

"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^', include('facturacion.urls')),
    url(r'^', include('producto.urls')),
    url(r'^admin/', admin.site.urls),
]
