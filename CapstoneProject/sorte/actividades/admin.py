from django.contrib import admin
from .models import Actividad
from .models import Inscripcion

# Register your models here.
admin.site.register(Actividad)

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['actividad', 'miembro', 'estado', 'fecha_solicitud']
    ordering = ['-fecha_solicitud']
    list_filter = ['estado']

admin.site.register(Inscripcion, InscripcionAdmin)