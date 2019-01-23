from django.db import models
from django.utils import timezone

# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField('fecha creacion', default=timezone.now())

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    lugar = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    fecha_inicio = models.DateTimeField('fecha inicio')
    fecha_fin = models.DateTimeField('fecha fin')
    es_presencial = models.BooleanField()
    fecha_creacion = models.DateTimeField('fecha creacion', default=timezone.now())

    def __str__(self):
        return self.nombre
