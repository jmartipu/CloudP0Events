from django.http import HttpResponse
from .models import Evento, Categoria
# Create your views here.


def index(request):
    lista_eventos = Evento.objects.order_by('-fecha_creacion')
    salida = '<br>'.join([("<a href=\"/eventos/evento/" + str(e.id) + "\">" + e.nombre + " " + e.categoria.nombre + " "
                           + str(e.fecha_creacion) + "</a>") for e in lista_eventos])
    return HttpResponse(salida)


def detalle_evento(request, evento_id):
    return HttpResponse("Detalle del evento %s." % evento_id)


