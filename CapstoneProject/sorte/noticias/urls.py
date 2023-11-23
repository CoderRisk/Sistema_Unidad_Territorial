from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_noticia, name="listar_noticia"),
    path('noticias/<int:pk>/', views.detalle_noticia.as_view(), name='detalle_noticia'),
    path('noticias/crear/', views.crear_noticia, name='crear_noticia'),
    path('noticias/editar/<int:pk>/', views.editar_noticia, name='editar_noticia'),
    path('noticias/eliminar/<int:pk>/', views.eliminar_noticia, name='eliminar_noticia'),
    path('noticias/carouselNoticias/<int:pk>/', views.carouselNoticias, name='carouselNoticias'),
]