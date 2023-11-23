from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Paths de la App Core
    path('', include('core.urls')),
    # Paths de la App Actividades de Django
    path('actividades/', include('actividades.urls')),
    # Paths de la App Noticias de Django
    path('noticias/', include('noticias.urls')),
    # Paths de la App Proyectos de Django
    path('proyectos/', include('proyectos.urls')),
    # Paths de la App Users de Django
    path('users/', include('users.urls')),
    # Paths de la App Dashboard de django
    path('dashboard/', include('dashboard.urls')),
    # Paths del Administrador de Django
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)