from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_proyecto, name="listar_proyectos"),
    path('proyectos/<int:pk>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('proyectos/editar/<int:pk>/', views.editar_proyecto, name='editar_proyecto'),
    path('proyectos/eliminar/<int:pk>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('mis_solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
    path('mis_solicitudes_aceptada/', views.mis_solicitudes_aceptada, name='mis_solicitudes_aceptada'),
    path('mis_solicitudes_rechazada/', views.mis_solicitudes_rechazada, name='mis_solicitudes_rechazada'),
    path('gestionar_solicitudes/', views.gestionar_solicitudes, name='gestionar_solicitudes'),
    path('gestionar_solicitudes_ver/<int:pk>', views.gestionar_solicitudes_ver, name='gestionar_solicitudes_ver'),
    path('gestionar_solicitudes_aceptada/', views.gestionar_solicitudes_aceptada, name='gestionar_solicitudes_aceptada'),
    path('gestionar_solicitudes_rechazada/', views.gestionar_solicitudes_rechazada, name='gestionar_solicitudes_rechazada'),
    path('inscribir/<int:proyecto_id>/', views.inscribir_proyecto, name='inscribir_proyecto'),
    path('proyectos/carouselProyectos/<int:pk>/', views.carouselProyectos, name='carouselProyectos'),
]