from django.db import models

# Create your models here.

class Carousel(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')
    fecha = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo
