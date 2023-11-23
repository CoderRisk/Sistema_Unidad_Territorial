from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('core/portal', views.portal, name="portal"),
    path('core/publicar', views.publicar, name="publicar"),
    path('core/carouselInicio/<int:pk>/', views.carouselInicio, name='carouselInicio'),
]