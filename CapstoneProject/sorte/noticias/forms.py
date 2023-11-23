from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = '__all__'
        widgets = {
            'imagen_noticia': forms.FileInput(attrs={'class': 'formulario__file'}),
            'titulo': forms.TextInput(attrs={'class': 'formulario__input'}),
            'subtitulo': forms.TextInput(attrs={'class': 'formulario__input'}),
            'descripcion': forms.Textarea(attrs={'class': 'formulario__area', 'rows': 2}),
            'fecha_de_creacion': forms.Select(attrs={'class': 'formulario__input'}),
            'fecha_de_actualizacion': forms.Select(attrs={'class': 'formulario__input'}),
        }