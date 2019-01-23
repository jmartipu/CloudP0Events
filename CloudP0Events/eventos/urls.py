from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('evento/<int:evento_id>', views.detalle_evento, name='detalle_evento'),
]
