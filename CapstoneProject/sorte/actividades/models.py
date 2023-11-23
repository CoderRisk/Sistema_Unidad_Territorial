from django.db import models
from users.models import CustomUSer

# Create your models here.
class Actividad(models.Model):
    imagen_actividad = models.ImageField(null=True, blank=True, upload_to="actividades")
    nombre_actividad = models.CharField(max_length=200)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=200)
    OPCIONES_REGION = (
        ('RM', 'Región Metropolitana'),
        # Aquí puedo seguir añadiendo REGIONES si es necesario
    )
    region = models.CharField(max_length=100, choices=OPCIONES_REGION, default='RM')
    OPCIONES_COMUNAS = (
        ('Isla de Maipo', 'Isla de Maipo'),
        # Aquí puedo seguir añadiendo COMUNAS si es necesario
    )
    comuna = models.CharField(max_length=100, choices=OPCIONES_COMUNAS, default='Isla de Maipo')
    fecha_creacion_actividad = models.DateTimeField(auto_now_add=True)
    fecha_actividad_tiempo_inicio = models.DateTimeField()
    fecha_actividad_tiempo_termino = models.DateTimeField()
    fecha_actividad = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    cupos_disponibles = models.IntegerField(default=0)

    class Meta:
        verbose_name = "actividad"
        verbose_name_plural = "actividades"

    def __str__(self):
        return self.nombre_actividad
    

class Inscripcion(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    miembro = models.ForeignKey(CustomUSer, on_delete=models.CASCADE)
    ESTADO_CHOICES = (
    ('pendiente', 'Pendiente'),
    ('aceptada', 'Aceptada'),
    ('rechazada', 'Rechazada'),
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')