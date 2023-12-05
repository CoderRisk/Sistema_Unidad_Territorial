from django import forms
from .models import Actividad, Inscripcion
from django.utils import timezone
from datetime import datetime

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'
        widgets = {
            'imagen_actividad': forms.FileInput(attrs={'class': 'formulario__file'}),
            'nombre_actividad': forms.TextInput(attrs={'class': 'formulario__input'}),
            'descripcion': forms.Textarea(attrs={'class': 'formulario__area', 'rows': 2}),
            'direccion': forms.TextInput(attrs={'class': 'formulario__input'}),
            'region': forms.Select(attrs={'class': 'formulario__select'}),
            'comuna': forms.Select(attrs={'class': 'formulario__select'}),
            'inicio_inscripcion': forms.DateInput(attrs={'class': 'formulario__input', 'type': 'datetime-local'}),
            'cierre_inscripcion': forms.DateInput(attrs={'class': 'formulario__input', 'type': 'datetime-local'}),
            'inicio_actividad': forms.DateInput(attrs={'class': 'formulario__input', 'type': 'date'}),
            'fin_actividad': forms.DateInput(attrs={'class': 'formulario__input', 'type': 'date'}),
            # 'hora_inicio': forms.TimeInput(attrs={'class': 'formulario__input', 'type': 'time'}),
            # 'hora_termino': forms.TimeInput(attrs={'class': 'formulario__input', 'type': 'time'}),
            'cupos_disponibles': forms.NumberInput(attrs={'class': 'formulario__input'}),
        }

    def clean_cupos_disponibles(self):
        cupos_disponibles = self.cleaned_data['cupos_disponibles']
        if cupos_disponibles <= 0:
            raise forms.ValidationError('La cantidad de cupos debe ser mayor a 0.')
        return cupos_disponibles
    

    # def clean_fecha_actividad(self):
    #     fecha_actividad = self.cleaned_data['fecha_actividad']

   
    #     return fecha_actividad
    
    # def clean_hora_inicio(self):
    #     # Acceder a los datos limpios de un campo específico
    #     # fecha_actividad = self.cleaned_data.get('fecha_actividad')
    #     fecha_inicio_hora_str = self.cleaned_data.get('hora_inicio')
        
    #     if fecha_inicio_hora_str is None:
    #         raise forms.ValidationError('Debe ingresar una fecha de actividad válida.')
  

    #     return fecha_inicio_hora_str
    
    # def clean_hora_termino(self):

    #      # Acceder a los datos limpios de un campo específico
    #     fecha_termino = self.cleaned_data.get('fecha_actividad')
    #     fecha_termino_hora_str = self.cleaned_data.get('hora_termino') 

    #     if fecha_termino is None:
    #         raise forms.ValidationError('Debe ingresar una fecha de actividad válida.')

    #     # Combinar la fecha y la hora
    #     # fecha_date_termino = datetime.combine(fecha_termino, fecha_termino_hora_str).time()

    #     # hora_actual_local = datetime.now(timezone.get_current_timezone()).time()

    #     # if fecha_date_termino < hora_actual_local:
    #     #     # Agregar un error al campo fecha_inicio
    #     #     raise forms.ValidationError('La hora de término no puede ser menor a la hora actual.')


    #     return fecha_termino_hora_str


class InscripcionForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    # archivos_adjuntos = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Inscripcion
        fields = ['nombre', 'apellido']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar el atributo readonly al campo mi_campo
        self.fields['nombre'].widget.attrs['readonly'] = True
        self.fields['apellido'].widget.attrs['readonly'] = True