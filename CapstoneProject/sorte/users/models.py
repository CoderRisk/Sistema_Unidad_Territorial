from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.
class CustomUSer(AbstractUser):
    username = models.CharField(max_length=50, null=True, unique=True, verbose_name='Nombre de usuario')
    rut = models.CharField(primary_key=True, max_length=12, verbose_name='Rut')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    birthdate = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'Prefiero no decirlo'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Género') 
    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.rut
    

class Certificado(models.Model):
    usuario = models.OneToOneField(get_user_model(), on_delete=models.CASCADE) # Existen .PROTECT - .SET_NULL - .SET_DEFAULT - .SET() - .DO_NOTHING.
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificado de {self.usuario.rut}"