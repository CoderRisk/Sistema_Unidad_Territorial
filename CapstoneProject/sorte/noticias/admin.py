from django.contrib import admin
from .models import Noticia

# Register your models here.
class NoticiaAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_de_creacion', 'fecha_de_actualizacion')

admin.site.register(Noticia, NoticiaAdmin)