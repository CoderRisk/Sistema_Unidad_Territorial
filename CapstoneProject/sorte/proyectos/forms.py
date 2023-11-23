from django.utils import timezone
from django import forms
from .models import Proyecto, Solicitud
from datetime import datetime

class TimeInputNoSeconds(forms.TimeInput):
    input_type = 'time'
    format = '%H:%M'


class ProyectoForm(forms.ModelForm):

    class Meta:
        model = Proyecto
        fields = '__all__'
        exclude = ['fecha_tiempo_inicio','fecha_date_termino']
        widgets = {
            'imagen_proyecto': forms.FileInput(attrs={'class': 'formulario__file'}),
            'nombre_proyecto': forms.TextInput(attrs={'class': 'formulario__input'}),
            'descripcion': forms.Textarea(attrs={'class': 'formulario__area', 'rows': 2}),
            'requisitos': forms.Textarea(attrs={'class': 'formulario__area', 'rows': 2}),
            'cupos_disponibles_proyecto': forms.NumberInput(attrs={'class': 'formulario__input'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'formulario__input', 'type': 'date'}),
            'fecha_inicio_hora': TimeInputNoSeconds(attrs={'class': 'formulario__input', 'type': 'time'}),
            'fecha_termino': forms.DateInput(attrs={'class': 'formulario__input', 'type': 'date'}),
            'fecha_termino_hora': TimeInputNoSeconds(attrs={'class': 'formulario__input', 'type': 'time'}),
            'fecha_creacion_proyecto': forms.DateInput(attrs={'class': 'formulario__input', 'type': 'date'}),
            'fecha_actualizacion_proyecto': forms.DateInput(attrs={'class': 'formulario__input', 'type': 'date'}),
        }

    def clean_cupos_disponibles_proyecto(self):
        cupos_disponibles = self.cleaned_data['cupos_disponibles_proyecto']
        if cupos_disponibles <= 0:
            raise forms.ValidationError('La cantidad de cupos debe ser mayor a 0.')
        return cupos_disponibles
    

    def clean_fecha_inicio(self):
     
        fecha_inicio = self.cleaned_data.get('fecha_inicio')

        if fecha_inicio == None:
            raise forms.ValidationError('Debe ingresar una fecha valida.')

        # if fecha_inicio < timezone.localtime(timezone.now()).date():
        #     raise forms.ValidationError('La fecha de inicio no puede ser anterior a la fecha actual.')

        return fecha_inicio
    

    def clean_fecha_inicio_hora(self):
        # Acceder a los datos limpios de un campo específico
        # fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_inicio_hora_ = self.cleaned_data.get('fecha_inicio_hora')

        # # Combinar la fecha y la hora
        # fecha_tiempo_inicio = datetime.combine(fecha_inicio, fecha_inicio_hora_str).time()

        # hora_actual_local = datetime.now(timezone.get_current_timezone()).time()

        # if fecha_tiempo_inicio < hora_actual_local:
        #     # Agregar un error al campo fecha_inicio_hora
        #     raise forms.ValidationError('La hora de inicio no puede ser menor a la hora actual.')
        if fecha_inicio_hora_ == None:
            raise forms.ValidationError('Debe ingresar una fecha valida.')

        return fecha_inicio_hora_


    def clean_fecha_termino(self):
     
        fecha_termino = self.cleaned_data.get('fecha_termino')

        if fecha_termino == None:
            raise forms.ValidationError('Debe ingresar una fecha valida.')

        # if fecha_termino < timezone.localtime(timezone.now()).date():
        #     raise forms.ValidationError('La fecha de término no puede ser anterior a la fecha actual.')

        return fecha_termino
    

    # def clean_fecha_termino_hora(self):

    #      # Acceder a los datos limpios de un campo específico
    #     fecha_termino = self.cleaned_data.get('fecha_termino')
    #     fecha_termino_hora_str = self.cleaned_data.get('fecha_termino_hora') 

    #     # Combinar la fecha y la hora
    #     fecha_date_termino = datetime.combine(fecha_termino, fecha_termino_hora_str).time()

    #     hora_actual_local = datetime.now(timezone.get_current_timezone()).time()

    #     if fecha_date_termino < hora_actual_local:
    #         # Agregar un error al campo fecha_inicio
    #         raise forms.ValidationError('La hora de término no puede ser menor a la hora actual.')


    #     return fecha_date_termino
    


# Formulario para postular a un proyecto
class PostulacionForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, required=True)
    apellido = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Solicitud
        fields = ['nombre', 'apellido']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'formulario__input'}),
            'apellido': forms.TextInput(attrs={'class': 'formulario__input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar el atributo readonly al campo mi_campo
        self.fields['nombre'].widget.attrs['readonly'] = True
        self.fields['apellido'].widget.attrs['readonly'] = True