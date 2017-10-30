from django.conf.urls import include, url
from . import views
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', views.render_login),
    url(r'^MenuDefault/$', views.menudefault),
    url(r'^Grupos/nuevo$', views.grupos_c),
    url(r'^Grupos/modificar$', views.grupos_u),
    url(r'^Usuarios/nuevo$', views.usuarios_c),
    url(r'^Usuarios/modificar$', views.usuarios_u),
    url(r'^Horarios/$', views.horarios),
    url(r'^Aulas/modificar$', views.aula_u),
    url(r'^Aulas/nuevo$', views.aula_c),
    url(r'^Ciclo_Escolar/$', views.cicloescolar),    
    url(r'^login/$', views.login),
    url(r'^crearUsuario/$', views.alta_usuario),
]
 