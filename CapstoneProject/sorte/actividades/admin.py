from django.contrib import admin
from .models import Actividad
from .models import Inscripcion, SolicitudInscripcion

# Register your models here.
admin.site.register(Actividad)

class SolicitudArchivoInline(admin.TabularInline):
    model = SolicitudInscripcion
    extra = 1

class InscripcionAdmin(admin.ModelAdmin):
    inlines = [SolicitudArchivoInline]
    list_display = ['actividad', 'miembro', 'estado', 'fecha_solicitud']
    ordering = ['-fecha_solicitud']
    list_filter = ['estado']
    exclude = ('archivos_adjuntos',)

admin.site.register(Inscripcion, InscripcionAdmin)