from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Carousel

# Create your views here.
def inicio(request):
    imagenes = Carousel.objects.all()

    return render(request, 'core/inicio.html', {'imagenes': imagenes})

def portal(request):
    return render(request, 'core/portal.html',)

def publicar(request):
    return render(request, 'core/publicar.html',)


def carouselInicio(request, pk):
     # Renderizar el template correspondiente y pasar la URL de la imagen
    imagen = get_object_or_404(Carousel, pk=pk)
    template = "core/verMas.html"

    return render(request, template, {'imagen': imagen})
