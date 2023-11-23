from django.contrib import admin
from .models import CustomUSer

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('rut', 'first_name', 'last_name', 'email', 'gender')

admin.site.register(CustomUSer, CustomUserAdmin)