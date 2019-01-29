from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'eventos'
urlpatterns = [
    path('', views.index, name='index'),
    path('lista_eventos/', views.lista_eventos_service, name='lista_eventos'),
    path('registro/', views.registro, name='registro'),
    path('adicionar_usuario/', views.adicionar_usuario, name='adicionar_usuario'),
    path('login/', views.login_service, name='login'),
    path('logout/', views.logout_service, name='logout'),
    path('evento/<int:evento_id>', views.detalle_evento, name='detalle_evento'),
    path('evento/<int:evento_id>/', views.detalle_evento, name='detalle_evento_con'),
    path('evento/<int:evento_id>/editar', views.editar_detalle_evento, name='editar_evento'),
    path('evento/<int:evento_id>/eliminar', views.eliminar_evento, name='eliminar_evento'),
    path('evento/crear_evento/', views.crear_evento_form, name='crear_evento'),
    path('evento/adicionar_evento/', views.adicionar_evento, name='adicionar_evento'),
]
