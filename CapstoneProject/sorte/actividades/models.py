from django.db import models
from users.models import CustomUSer
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

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
    inicio_inscripcion = models.DateTimeField()
    cierre_inscripcion = models.DateTimeField()
    inicio_actividad = models.DateField()
    fin_actividad = models.DateField()
    # fecha_actividad_tiempo_inicio = models.DateTimeField()
    # fecha_actividad_tiempo_termino = models.DateTimeField()
    # fecha_actividad = models.DateField()
    # hora_inicio = models.TimeField()
    # hora_termino = models.TimeField()
    cupos_disponibles = models.IntegerField(default=0)

    class Meta:
        verbose_name = "actividad"
        verbose_name_plural = "actividades"

    def __str__(self):
        return self.nombre_actividad
    

def ruta_solicitudes_archivos(instance, filename):
    # Obtiene el id de la solicitud y el nombre del archivo original
    solicitud_id = instance.campo_inscripcion.id
    nombre_original, extension = os.path.splitext(filename)
    
    # Construye la ruta única para cada archivo adjunto
    ruta = f'solicitudes_inscripciones/inscripcion_{solicitud_id}/{nombre_original}_{extension}'
    
    return ruta    
    

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
    archivos_adjuntos = models.ManyToManyField('SolicitudInscripcion', blank=True, related_name='archivos_adjuntos')

@receiver(pre_delete, sender=Inscripcion)
def eliminar_archivos_solicitud(sender, instance, **kwargs):
    # Eliminar archivos asociados a la solicitud al eliminar la solicitud
    archivos_solicitud = SolicitudInscripcion.objects.filter(campo_inscripcion=instance)
    for archivo_solicitud in archivos_solicitud:
        archivo_solicitud.delete()

    # Eliminar la carpeta si está vacía
    carpeta_ruta = os.path.join('media', 'archivos_solicitudes', f'solicitud_{instance.id}')
    if os.path.exists(carpeta_ruta) and not os.listdir(carpeta_ruta):
        os.rmdir(carpeta_ruta)
class SolicitudInscripcion(models.Model):
    campo_inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to=ruta_solicitudes_archivos)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.archivo.name
    
@receiver(pre_delete, sender=SolicitudInscripcion)
def eliminar_archivo_solicitud(sender, instance, **kwargs):
    # Eliminar el archivo físico del sistema de archivos
    archivo_ruta = instance.archivo.path
    if os.path.exists(archivo_ruta):
        os.remove(archivo_ruta)