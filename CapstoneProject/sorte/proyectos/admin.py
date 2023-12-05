from django.contrib import admin
from .models import Proyecto, Solicitud, SolicitudArchivo

class SolicitudArchivoInline(admin.TabularInline):
    model = SolicitudArchivo
    extra = 1

class SolicitudAdmin(admin.ModelAdmin):
    inlines = [SolicitudArchivoInline]
    list_display = ('id', 'miembro', 'proyecto', 'estado', 'fecha_solicitud')
    exclude = ('archivos_adjuntos',)



# Register your models here.
admin.site.register(Proyecto)
admin.site.register(Solicitud, SolicitudAdmin)