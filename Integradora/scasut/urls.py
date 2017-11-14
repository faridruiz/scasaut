from django.conf.urls import include, url
from . import views
from django.core.urlresolvers import reverse_lazy

 
urlpatterns = [
    url(r'^$', views.start), #vista creada
    url(r'^login/$', views.login), #vista creada
    url(r'^login/verificar$', views.login_verificar), #vista creada
    url(r'^dashboard/$', views.dashboard), #vista creada

    url(r'^usuarios/nuevo$', views.usuarios_nuevo), #vista creada
    url(r'^usuarios/nuevo/crear$', views.usuarios_nuevo_crear), #vista creada
    url(r'^usuarios/$', views.usuarios), #vista creada
    url(r'^usuarios/edicion/(?P<id>\d+)$', views.usuarios_edicion),
    url(r'^usuarios/edicion/modificar/(?P<id>\d+)$', views.usuarios_edicion_modificar), #vista creada
    url(r'^usuarios/edicion/eliminar/(?P<id>\d+)$', views.usuarios_edicion_eliminar), #vista creada

    url(r'^aulas/nuevo$', views.aulas_nuevo),
    url(r'^aulas/nuevo/crear$', views.aulas_nuevo_crear),
    url(r'^aulas/$', views.aulas),
    url(r'^aulas/edicion/(?P<id>\d+)$', views.aulas_edicion),
    url(r'^aulas/edicion/modificar/(?P<id>\d+)$', views.aulas_edicion_modificar),
    url(r'^aulas/edicion/eliminar/(?P<id>\d+)$', views.aulas_edicion_eliminar),

    url(r'^grupos/nuevo$', views.grupos_nuevo),
    url(r'^grupos/nuevo/crear$', views.grupos_nuevo_crear),
    url(r'^grupos/$', views.grupos),
    url(r'^grupos/edicion/(?P<id>\d+)$', views.grupos_edicion),
    url(r'^grupos/edicion/modificar/(?P<id>\d+)$', views.grupos_edicion_modificar),
    url(r'^grupos/edicion/eliminar/(?P<id>\d+)$', views.grupos_edicion_eliminar),
    url(r'^verificarPin/(?P<pin>\d+)$', views.verificarPin),
    url(r'^registroHuella/(?P<pin>\d+)$', views.registroHuella),
    url(r'^scheduler/$', views.scheduler),
#    url(r'^horarios/$', views.horarios),
#    url(r'^horarios/nuevo/(?P<id>\d+)$', views.horarios_nuevo),
#    url(r'^horarios/edicion/(?P<id>\d+)$', views.horarios_edicion),
#    url(r'^horarios/eliminar/(?P<id>\d+)$', views.horarios_eliminar),

#    url(r'^cicloescolar/$', views.cicloescolar),
#    url(r'^cicloescolar/nuevo/(?P<id>\d+)$', views.cicloescolar_nuevo),
#    url(r'^cicloescolar/edicion/(?P<id>\d+)$', views.cicloescolar_edicion),
#    url(r'^cicloescolar/eliminacion/(?P<id>\d+)$', views.cicloescolar_eliminacion),

]