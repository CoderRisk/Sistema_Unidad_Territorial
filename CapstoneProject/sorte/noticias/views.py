from django.shortcuts import render, get_object_or_404, redirect
from .models import Noticia
from .forms import NoticiaForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from typing import Any
from core.models import Carousel

# Listar Noticias
def listar_noticia(request):
    imagenes = Carousel.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        noticias = Noticia.objects.filter(
            Q(titulo__icontains=q) | 
            Q(subtitulo__icontains=q) |
            Q(descripcion__icontains=q)).order_by('-fecha_de_creacion')
        paginator = Paginator(noticias, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        noticias = Noticia.objects.all().order_by('-fecha_de_creacion')
        paginator = Paginator(noticias, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    return render(request, "noticias/listar_noticia.html", {
        'page_obj': page_obj,
        'imagenes': imagenes,
    })

# --------------------------------------------------------------------------------------------

# Detalle de actividad
class detalle_noticia(DetailView):
    model = Noticia
    template_name = 'noticias/detalle_noticia.html'

   
# --------------------------------------------------------------------------------------------

# Crear actividad
@staff_member_required
def crear_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu noticia ha sido creada con exito')
            return redirect('listar_noticia')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/crear_noticia.html', {'form': form})

# --------------------------------------------------------------------------------------------

# Editar actividad
@staff_member_required
def editar_noticia(request, pk):
    noticias = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticias)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu noticia ha sido editada con exito.')
            return redirect('listar_noticia')
    else:
        form = NoticiaForm(instance=noticias)
    return render(request, 'noticias/editar_noticia.html', {'form': form, 'noticias': noticias})

# --------------------------------------------------------------------------------------------

# Eliminar actividad
@staff_member_required
def eliminar_noticia(request, pk):
    noticias = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        noticias.delete()
        messages.success(request, '¡La Noticia ha sido eliminada correctamente!')
        return redirect('listar_noticia')
    return render(request, 'noticias/eliminar_noticia_confirmar.html', {'noticias': noticias})

# --------------------------------------------------------------------------------------------------

def carouselNoticias(request, pk):
     # Renderizar el template correspondiente y pasar la URL de la imagen
    imagen = get_object_or_404(Carousel, pk=pk)
    template = "noticias/carouselNoticias.html"

    return render(request, template, {'imagen': imagen})