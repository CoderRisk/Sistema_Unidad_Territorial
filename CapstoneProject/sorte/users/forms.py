from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUSer, Certificado
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(min_length=1, max_length=50, required=True)
    last_name = forms.CharField(min_length=1, max_length=50, required=True)
    email = forms.EmailField(label='Correo Electrónico', required=True, widget=forms.EmailInput(attrs={'class': 'formulario__input'}))
    address = forms.CharField(max_length=200, required=True)
    birthdate = forms.DateField()
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'Prefiero no decirlo'),
    )
    gender = forms.ChoiceField(label='Género', choices=GENDER_CHOICES, required=True, widget=forms.RadioSelect)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, required=True, 
            error_messages={
            'required': 'Por favor, completa el reCAPTCHA para continuar.'
        })
    
    def clean_rut(self):

        rut = self.cleaned_data.get('rut')

        if CustomUSer.objects.filter(rut=rut):
            raise forms.ValidationError('El RUT ya existe.')
        
        return rut

    # Validador de contraseñas
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        errors = []

        # Agrega tus propias reglas de validación aquí
        if len(password1) < 8:
            errors.append(forms.ValidationError('La contraseña debe tener al menos 8 caracteres.'))
            
        if password1 and password2 and password1 != password2:
            errors.append(forms.ValidationError('Las contraseñas no coinciden. Por favor, inténtalo nuevamente.'))
        
        if not any(char.isdigit() for char in password1):
            errors.append(forms.ValidationError('La contraseña debe contener al menos un número.'))

        if not any(char.isalpha() for char in password1):
            errors.append(forms.ValidationError('La contraseña debe contener al menos una letra.'))

        if errors:
            raise forms.ValidationError(errors)
        
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        errors = []

        # Agrega tus propias reglas de validación aquí
        if len(password2) < 8:
            errors.append(forms.ValidationError('La contraseña debe tener al menos 8 caracteres.'))
            
        if password2 and password1 and password2 != password1:
            errors.append(forms.ValidationError('Las contraseñas no coinciden. Por favor, inténtalo nuevamente.'))
        
        if not any(char.isdigit() for char in password2):
            errors.append(forms.ValidationError('La contraseña debe contener al menos un número.'))

        if not any(char.isalpha() for char in password2):
            errors.append(forms.ValidationError('La contraseña debe contener al menos una letra.'))

        if errors:
            raise forms.ValidationError(errors)

        return password2

    
    
    # Validar si el email ya existe en la base de datos
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUSer.objects.filter(email__iexact=email).exists():
            raise ValidationError('Este correo ya existe.')
        return email
    
    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        
        if not gender:
            raise ValidationError("Este campo no puede dejarse vacío. Por favor, selecciona una opción.")
        return gender
    
    def clean_address(self):
        address = self.cleaned_data.get('address')

        if not address:
            raise ValidationError("Este campo no puede dejarse vacío. Por favor, selecciona una opción.")
        return address

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')

        fecha_actual = datetime.now().date()
  
        fecha_resultado = fecha_actual.year - birthdate.year;

        if not birthdate:
            raise ValidationError("Este campo no puede dejarse vacío. Por favor, selecciona una opción.")
        elif fecha_resultado < 14:
            raise ValidationError("Tienes que ser mayor de 18 años")
        return birthdate       
    

    class Meta:
        model = CustomUSer
        fields = ('rut', 'first_name', 'last_name', 'birthdate', 'address', 'email', 'gender', 'password1', 'password2')


# Formulario para la actualización de los datos de usuarios registrados
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUSer
        fields = ['first_name', 'last_name', 'email']


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs=
            {'class': 'formulario__input',
             'placeholder': 'Ej: correo@correo.com'}),
        label='Correo Electrónico',
    )

class UserPasswordResetConfirmForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'nueva contraseña'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'confirmar contraseña'})


    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')

        # Obtenemos el usuario actual
        user = self.user

        # Verificamos que la nueva contraseña no sea igual a la contraseña actual
        if user.check_password(new_password1):
            raise forms.ValidationError('La nueva contraseña no puede ser igual a la contraseña actual.')

        # Verificamos que la nueva contraseña no sea igual a contraseñas antiguas
        if User.objects.filter(rut=user.rut, password=new_password1).exists():
            raise forms.ValidationError('La nueva contraseña no puede ser igual a contraseñas antiguas.')

        return new_password1



    # contrasena1 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'formulario__input',
    #             'placeholder': 'Nueva Contraseña'
    #             }
    #         ),
    #         label = 'Nueva Contraseña',
    #         help_text=(
    #         '<ul>'
    #         '<li>Su contraseña no puede asemejarse tanto a su otra información personal.</li>'
    #         '<li>Su contraseña debe contener al menos 8 caracteres.</li>'
    #         '<li>Su contraseña no puede ser una clave utilizada comúnmente.</li>'
    #         '<li>Su contraseña no puede ser completamente numérica.</li>'
    #         '</ul>'
    #     ))
    
    # contrasena2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             'class': 'formulario__input',
    #             'placeholder': 'Confirmar Contraseña'
    #         }
    #     ),
    #     label = 'Nueva Contraseña'
    # )
    
    
