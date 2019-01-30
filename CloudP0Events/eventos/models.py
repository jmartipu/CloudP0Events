from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

# Create your models here.



class UserForm(ModelForm):

    username = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'password2']


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateField('fecha creacion')
    hora_creacion = models.TimeField('hora creacion')
    usuario_creacion = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    lugar = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    fecha_inicio = models.DateField('fecha inicio')
    fecha_fin = models.DateField('fecha fin')
    es_presencial = models.BooleanField()
    fecha_creacion = models.DateField('fecha creacion')
    hora_creacion = models.TimeField('hora creacion')
    usuario_creacion = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre


class EventoForm(ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'categoria', 'lugar', 'direccion', 'fecha_inicio', 'fecha_fin', 'es_presencial']

