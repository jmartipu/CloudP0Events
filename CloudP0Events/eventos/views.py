from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_list_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Evento, UserForm, Categoria, EventoForm
from django.utils import timezone

# Create your views here.


def index(request):
    return render(request, "eventos/index.html")


def registro(request):
    if not request.user.is_authenticated:
        form = UserForm
        return render(request, 'eventos/registro.html', {'form': form})
    return HttpResponseRedirect(reverse('eventos:index'))

@csrf_exempt
def adicionar_usuario(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            user_existe = User.objects.get(username=username)
        except:
            user_existe = None

        if user_existe is None:
            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.save()
            messages.success(request, "Usuario creado con exito!", extra_tags='alert alert-success')
            ruta = 'eventos:index'

        else:
            messages.warning(request, "No se puede crear el usuario, porque ya existe.", extra_tags='alert alert-warning')
            ruta = 'eventos:registro'
    else:
        ruta = 'eventos:index'
    return HttpResponseRedirect(reverse(ruta))


@csrf_exempt
def login_service(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            usuario = request.POST.get('usuario')
            contrasena = request.POST.get('contrasena')
            user = authenticate(username=usuario, password=contrasena)
            if user is not None:
                login(request, user)
            else:
                messages.error(request, "Usuario o contraeña inválidos.", extra_tags='alert alert-danger')

    return HttpResponseRedirect(reverse('eventos:index'))


def logout_service(request):
    logout(request)
    return HttpResponseRedirect(reverse('eventos:index'))


@csrf_exempt
def lista_eventos_service(request):
    if request.user.is_authenticated:
        usuario = User.objects.filter(username=request.user).first()
        lista = Evento.objects.filter(usuario_creacion=usuario).order_by('-fecha_creacion', '-hora_creacion')
        return HttpResponse(serializers.serialize("json", lista))
    return HttpResponseRedirect(reverse('eventos:index'))


def detalle_evento(request, evento_id):
    if request.user.is_authenticated:
        usuario_autenticado = User.objects.filter(username=request.user).first()
        if usuario_autenticado is not None:
            evento_seleccionado = Evento.objects.filter(id=evento_id, usuario_creacion=usuario_autenticado).first()
            if evento_seleccionado is not None:
                lista_categorias = get_list_or_404(Categoria)
                form = EventoForm
                form.nombre = evento_seleccionado.nombre

                context = {
                    'evento_seleccionado': evento_seleccionado,
                    'lista_categorias': lista_categorias,
                    'form': form,
                }
                return render(request, 'eventos/detalle.html', context)
            else:
                messages.warning(request, "No se tiene permiso para visualizar el evento seleccionado", extra_tags='alert alert-warning')
    return HttpResponseRedirect(reverse('eventos:index'))


def editar_detalle_evento(request, evento_id):
    if request.user.is_authenticated:
        usuario_autenticado = User.objects.filter(username=request.user).first()
        if usuario_autenticado is not None:
            evento_editar = Evento.objects.filter(id=evento_id, usuario_creacion=usuario_autenticado).first()
            if evento_editar is not None:
                try:
                    evento_editar.nombre = request.POST['nombre']
                    categoria_seleccionada = Categoria.objects.filter(id=request.POST['categoria']).first()
                    evento_editar.categoria = categoria_seleccionada
                    evento_editar.lugar = request.POST['lugar']
                    evento_editar.direccion = request.POST['direccion']
                    evento_editar.fecha_inicio = request.POST['finicio']
                    evento_editar.fecha_fin = request.POST['ffin']
                    evento_editar.es_presencial = True if request.POST.get('es_presencial', None) else False
                    evento_editar.save()
                    messages.success(request, "Evento editado con exito!", extra_tags='alert alert-success')
                except:
                    messages.error(request, "Error al editar el evento!", extra_tags='alert alert-danger')

            else:
                messages.error(request, "Error al editar el evento!", extra_tags='alert alert-danger')
    return HttpResponseRedirect(reverse('eventos:index'))


def crear_evento_form(request):
    form = EventoForm
    lista_categorias = get_list_or_404(Categoria)

    context = {
        'lista_categorias': lista_categorias,
        'form': form,
    }
    return render(request, 'eventos/crear_evento.html', context)


@csrf_exempt
def adicionar_evento(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            categoria = Categoria.objects.filter(id=request.POST.get('categoria')).first()
            lugar = request.POST.get('lugar')
            direccion = request.POST.get('direccion')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            if request.POST.get('es_presencial') == 'on':
                bool_presencial = True
            else:
                bool_presencial = False

            usuario_creacion = User.objects.filter(username=request.user).first()
            if usuario_creacion is not None and categoria is not None:
                try:
                    evento_existe = Evento.objects.get(nombre=nombre, categoria=categoria, lugar=lugar,
                                                       direccion=direccion, fecha_inicio=fecha_inicio,
                                                       fecha_fin=fecha_fin, es_presencial=bool_presencial,
                                                       usuario_creacion=usuario_creacion)
                except:
                    evento_existe = None

                if evento_existe is None:
                    try:
                        evento_model = Evento(nombre=nombre, categoria=categoria, lugar=lugar, direccion=direccion,
                                              fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
                                              fecha_creacion=timezone.now().date(), hora_creacion=timezone.now().strftime("%H:%M:%S"),
                                              es_presencial=bool_presencial,
                                              usuario_creacion=usuario_creacion)

                        evento_model.save()
                        messages.success(request, "Evento creado con exito!", extra_tags='alert alert-success')
                    except:
                        messages.error(request, "Error creando evento!", extra_tags='alert alert-danger')

                    ruta = 'eventos:index'

                else:
                    messages.warning(request, "No se puede crear el evento, porque ya existe.", extra_tags='alert alert-warning')
                    ruta = 'eventos:index'
            else:
                messages.warning(request, "No existe el usuario o la categoria", extra_tags='alert alert-warning')
                ruta = 'eventos:index'
    else:
        messages.warning(request, "No tiene permisos para crear el evento.", extra_tags='alert alert-warning')
        ruta = 'eventos:index'

    return HttpResponseRedirect(reverse(ruta))


def eliminar_evento(request, evento_id):
    if request.user.is_authenticated:
        usuario_autenticado = User.objects.filter(username=request.user).first()
        if usuario_autenticado is not None:
            evento_eliminar = Evento.objects.filter(id=evento_id, usuario_creacion=usuario_autenticado).first()

            if evento_eliminar is not None:
                try:
                    evento_eliminar.delete()
                    messages.success(request, "Evento eliminado con exito!", extra_tags='alert alert-success')
                except:
                    messages.error(request, "Error al eliminar el evento!", extra_tags='alert alert-danger')

            else:
                messages.error(request, "Error al eliminar el evento!", extra_tags='alert alert-danger')
    return HttpResponseRedirect(reverse('eventos:index'))
