from django.db import models
from users.models import CustomUSer
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os


# Create your models here.
class Proyecto(models.Model):
    imagen_proyecto = models.ImageField(null=True, blank=True, upload_to="proyectos")
    nombre_proyecto = models.CharField(max_length=100)
    descripcion = models.TextField()
    requisitos = models.TextField()
    cupos_disponibles_proyecto = models.IntegerField(default=0)
    inicio_postulacion = models.DateTimeField()
    # fecha_inicio = models.DateField()
    # fecha_inicio_hora = models.TimeField()
    cierre_postulacion = models.DateTimeField()
    # fecha_termino = models.DateField()
    # fecha_termino_hora = models.TimeField()
    inicio_del_proyecto = models.DateField()
    fin_del_proyecto = models.DateField()
    fecha_creacion_proyecto = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion_proyecto = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización del proyecto')

    class Meta:
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"

    def __str__(self):
        return self.nombre_proyecto
    


def ruta_solicitudes_archivos(instance, filename):
    # Obtiene el id de la solicitud y el nombre del archivo original
    solicitud_id = instance.campo_solicitud.id
    nombre_original, extension = os.path.splitext(filename)
    
    # Construye la ruta única para cada archivo adjunto
    ruta = f'archivos_solicitudes/solicitud_{solicitud_id}/{nombre_original}_{extension}'
    
    return ruta    
    
# Añadiendo un modelo para las solicitudes de postulación
class Solicitud(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    miembro = models.ForeignKey(CustomUSer, on_delete=models.CASCADE)
    ESTADO_CHOICES = (
    ('pendiente', 'Pendiente'),
    ('aceptada', 'Aceptada'),
    ('rechazada', 'Rechazada'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    archivos_adjuntos = models.ManyToManyField('SolicitudArchivo', blank=True, related_name='archivos_adjuntos')

    def __str__(self):
        return f"Solicitud de {self.miembro.username} para {self.proyecto.nombre_proyecto}"


@receiver(pre_delete, sender=Solicitud)
def eliminar_archivos_solicitud(sender, instance, **kwargs):
    # Eliminar archivos asociados a la solicitud al eliminar la solicitud
    archivos_solicitud = SolicitudArchivo.objects.filter(campo_solicitud=instance)
    for archivo_solicitud in archivos_solicitud:
        archivo_solicitud.delete()

    # Eliminar la carpeta si está vacía
    carpeta_ruta = os.path.join('media', 'archivos_solicitudes', f'solicitud_{instance.id}')
    if os.path.exists(carpeta_ruta) and not os.listdir(carpeta_ruta):
        os.rmdir(carpeta_ruta)

class SolicitudArchivo(models.Model):
    campo_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to=ruta_solicitudes_archivos)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.archivo.name
    

@receiver(pre_delete, sender=SolicitudArchivo)
def eliminar_archivo_solicitud(sender, instance, **kwargs):
    # Eliminar el archivo físico del sistema de archivos
    archivo_ruta = instance.archivo.path
    if os.path.exists(archivo_ruta):
        os.remove(archivo_ruta)

    


    

