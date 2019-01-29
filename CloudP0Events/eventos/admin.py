from django.contrib import admin
from .models import Categoria, Evento

# Register your models here.


class CategoriaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre', 'usuario_creacion']}),
        ('Date information', {'fields': ['fecha_creacion']}),
    ]


class EventoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nombre', 'categoria', 'usuario_creacion']}),
        ('Información de lugar', {'fields': ['lugar', 'direccion', 'es_presencial']}),
        ('Información de fechas', {'fields': ['fecha_inicio', 'fecha_fin', 'fecha_creacion']}),
    ]


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Evento, EventoAdmin)
