from django.db import models

# Create your models here.
class Noticia(models.Model):
    imagen_noticia = models.ImageField(null=True, blank=True, upload_to="noticias")
    titulo = models.CharField(max_length=200)
    subtitulo = models.TextField()
    descripcion = models.TextField()
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    fecha_de_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "noticia"
        verbose_name_plural = "noticias"
    
    def __str__(self):
        return self.titulo