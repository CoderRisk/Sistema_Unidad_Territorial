from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto, Solicitud
from .forms import ProyectoForm
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .forms import PostulacionForm
from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from core.models import Carousel
from django.utils import timezone
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

#--------------------------------------------------------------------------------------------

# Listar Proyectos
def listar_proyecto(request):
    imagenes = Carousel.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        proyectos = Proyecto.objects.filter(
            Q(nombre_proyecto__icontains=q) | 
            Q(descripcion__icontains=q)).order_by('-fecha_creacion_proyecto')
        paginator = Paginator(proyectos, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        proyectos = Proyecto.objects.all().order_by('-fecha_creacion_proyecto')
        paginator = Paginator(proyectos, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    return render(request, "proyectos/listar_proyectos.html", {
        'page_obj': page_obj,
        'imagenes': imagenes
    })

#--------------------------------------------------------------------------------------------

# Detalle Proyecto
def detalle_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    return render(request, 'proyectos/detalle_proyecto.html', {
        'proyecto': proyecto
    })

#--------------------------------------------------------------------------------------------

# Crear Proyecto
@staff_member_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            proyecto = form.save(commit=False)

            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_inicio_hora = form.cleaned_data['fecha_inicio_hora']
            fecha_tiempo_inicio = datetime.combine(fecha_inicio, fecha_inicio_hora)

            fecha_termino = form.cleaned_data['fecha_termino']
            fecha_termino_hora = form.cleaned_data['fecha_termino_hora']
            fecha_date_termino = datetime.combine(fecha_termino, fecha_termino_hora)

            # Validación personalizada para asegurarse de que la fecha de inicio sea anterior a la fecha de término
            if fecha_inicio > fecha_termino:
                form.add_error('fecha_inicio', 'La fecha de inicio debe ser menor a la fecha de término.')

            if fecha_termino < fecha_inicio:
                form.add_error('fecha_termino', 'La fecha de término debe ser menor a la fecha de inicio.')

            if fecha_inicio_hora >= fecha_termino_hora:
                form.add_error('fecha_inicio_hora', 'La hora de inicio debe ser menor a la hora de término.')

            if fecha_termino_hora <= fecha_inicio_hora:
                form.add_error('fecha_termino_hora', 'La hora de término debe ser mayor a la hora de inicio.')

            # Otras validaciones personalizadas aquí...

            if form.errors:
                # Si hay errores, renderiza nuevamente el formulario con los errores personalizados.
                return render(request, 'proyectos/crear_proyecto.html', {'form': form})

            # Resto del código...

            proyecto.fecha_tiempo_inicio = fecha_tiempo_inicio
            proyecto.fecha_date_termino = fecha_date_termino
            proyecto.save()

            messages.success(request, '¡El proyecto ha sido creado con éxito!')
            return redirect('listar_proyectos')

        else:
            print(form)

    else:
        form = ProyectoForm()

    return render(request, 'proyectos/crear_proyecto.html', {'form': form})

#--------------------------------------------------------------------------------------------

# Editar Proyecto
@staff_member_required
def editar_proyecto(request, pk):
    proyectos = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES, instance=proyectos)
        print(form.errors)
        if form.is_valid():
            
            # Combina fecha y hora antes de guardar en el modelo
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_inicio_hora = form.cleaned_data['fecha_inicio_hora']
            fecha_tiempo_inicio = datetime.combine(fecha_inicio, fecha_inicio_hora)

            fecha_termino = form.cleaned_data['fecha_termino']
            fecha_termino_hora = form.cleaned_data['fecha_termino_hora']
            fecha_date_termino = datetime.combine(fecha_termino, fecha_termino_hora)

            # Validación personalizada para asegurarse de que la fecha de inicio sea anterior a la fecha de término
            if fecha_inicio > fecha_termino:
                form.add_error('fecha_inicio', 'La fecha de inicio debe ser menor a la fecha de término.')

            if fecha_termino < fecha_inicio:
                form.add_error('fecha_termino', 'La fecha de término debe ser menor a la fecha de inicio.')

            if fecha_inicio_hora >= fecha_termino_hora:
                form.add_error('fecha_inicio_hora', 'La hora de inicio debe ser menor a la hora de término.')

            if fecha_termino_hora <= fecha_inicio_hora:
                form.add_error('fecha_termino_hora', 'La hora de término debe ser mayor a la hora de inicio.')

            # Otras validaciones personalizadas aquí...

            if form.errors:
                # Si hay errores, renderiza nuevamente el formulario con los errores personalizados.
                return render(request, 'proyectos/editar_proyecto.html', {'form': form, 'proyectos': proyectos})

            # Actualiza el campo en el modelo
            proyectos.fecha_tiempo_inicio = fecha_tiempo_inicio
            proyectos.fecha_date_termino = fecha_date_termino

            form.save()

            proyecto = proyectos.fecha_actualizacion_proyecto
            # proyecto = timezone.localtime(proyecto)

            print(proyecto)
            messages.success(request, '¡El proyecto ha sido editado correctamente!')
            return redirect('listar_proyectos')
        else:
             # Acceder a los datos limpios de un campo específico
            print('si')
            fecha_inicio = form.data.get('fecha_inicio')
            fecha_inicio_hora = form.data.get('fecha_inicio_hora')
            fecha_termino = form.data.get('fecha_termino')
            fecha_termino_hora = form.data.get('fecha_termino_hora')

            if fecha_inicio and fecha_termino and fecha_inicio > fecha_termino:
                # Agregar un error al campo fecha_inicio
                form.add_error('fecha_inicio', 'La fecha de inicio no puede ser posterior a la fecha de término.')

            if fecha_inicio_hora and fecha_termino_hora and fecha_inicio_hora > fecha_termino_hora:
                form.add_error('fecha_inicio_hora', 'La hora de inicio no puede ser posterior a la hora de término.')

            if fecha_inicio and fecha_termino and fecha_termino < fecha_inicio:
                # Agregar un error al campo fecha_inicio
                form.add_error('fecha_termino', 'La fecha de término no puede ser anterior a la fecha de inicio.')

            if fecha_termino_hora and fecha_inicio_hora and fecha_termino_hora < fecha_inicio_hora:
                form.add_error('fecha_termino_hora', 'La hora de término no puede ser posterior a la hora de inicio.')
    else:
        form = ProyectoForm(instance=proyectos)
    return render(request, 'proyectos/editar_proyecto.html', {'form': form, 'proyectos': proyectos})

#--------------------------------------------------------------------------------------------

# Eliminar Proyecto
@staff_member_required
def eliminar_proyecto(request, pk):
    proyectos = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyectos.delete()
        messages.success(request, '¡El proyecto ha sido eliminado correctamente!')
        return redirect('listar_proyectos')
    return render(request, 'proyectos/eliminar_proyecto_confirmar.html', {'proyectos': proyectos})

#--------------------------------------------------------------------------------------------

# Vista para la inscripción de proyectos
@login_required
def inscribir_proyecto(request, proyecto_id):
    proyecto = Proyecto.objects.get(id=proyecto_id)

    if proyecto.cupos_disponibles_proyecto > 0:
        if request.method == 'POST':
            form = PostulacionForm(request.POST)
            if form.is_valid():
                solicitud = form.save(commit=False)
                solicitud.proyecto = proyecto
                solicitud.miembro = request.user
                solicitud.estado = 'pendiente'
                

                # Verifica si el usuario ya ha postulado al proyecto
                solicitud_existente = Solicitud.objects.filter(proyecto=proyecto, miembro=request.user).first()

                if solicitud_existente is not None:
                    messages.error(request, 'Lo sentimos, pero ya has enviado una solicitud para este proyecto')
                else:
                    solicitud.save()
                    solicitud.fecha_solicitud = datetime.now()

                    # Disminuir cupos de proyectos
                    # proyecto.cupos_disponibles_proyecto -= 1
                    proyecto.save()

                    # Obteniendo la fecha y hora actual
                    fecha_actual = datetime.now().strftime("%d-%m-%Y")
                    hora_actual = datetime.now().strftime("%H:%M:%S")

                    messages.success(request, 'Tu solicitud ha sido enviada y será gestionada por nuestra directiva.')
                    send_mail(
                        'Confirmación de Solicitud', 
                        f'Hola {request.user.first_name} {request.user.last_name},\n\n'
                        f'Con fecha {fecha_actual} y hora {hora_actual} te informamos que tu solicitud ' 
                        f'al proyecto {proyecto.nombre_proyecto} ha sido recibida y será gestionada por nuestra directiva. '
                        f'Te confirmaremos si fue aceptada o rechazada por correo.\n\n¡Muchas Gracias!\n\nSORTE', 
                        'cuentaprueba4326@gmail.com',
                        [request.user.email]
                    )
                    return redirect("mis_solicitudes")
        else:
            form = PostulacionForm(initial={'nombre': request.user.first_name, 'apellido': request.user.last_name})
        
        return render(request, 'proyectos/inscripcion_proyecto.html', {'form': form, 'proyecto': proyecto})
    else:
        # Obteniendo la fecha y hora actual
        fecha_actual = datetime.now().strftime("%d - %m - %Y")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        messages.error(request, 'Lo sentimos, pero ya no hay cupos disponibles para este proyecto.')
        send_mail(
            'Cupos Agotados',
            f'Hola {request.user.first_name} {request.user.last_name},\n\nCon fecha {fecha_actual} y hora {hora_actual} damos respuesta a tu solicitud para '
            f'comunicarte que el proyecto con nombre {proyecto.nombre_proyecto} no tiene cupos disponibles.\n\nLamentamos los inconvenientes\n\nSORTE',
            'cuentaprueba4326@gmail.com',
            [request.user.email]
        )
        return redirect('listar_proyectos')
    
# ----------------------------------------------------------------------------------

@staff_member_required
def gestionar_solicitudes(request):
    if not request.user.is_staff:
        return redirect('inicio')
    
    # solicitudes = Solicitud.objects.all()
    # proyecto = Solicitud.objects.filter(
    #     Q(proyecto__id=id) | Q(rut=S)
    # )


    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        
        decision = request.POST.get('decision')
        solicitud = Solicitud.objects.get(id=solicitud_id)

        if decision == 'aceptar':
            solicitud.estado = 'aceptada'
            proyecto = solicitud.proyecto

            if proyecto.cupos_disponibles_proyecto > 0:
                proyecto.cupos_disponibles_proyecto -= 1

                if proyecto.cupos_disponibles_proyecto == 0:
                    # Obtener la URL inversa basada en el nombre del patrón de URL
                    url = reverse('gestionar_solicitudes')
                    proyecto.save()
                    solicitud.save()
                    Solicitud.objects.filter(proyecto=proyecto, estado='pendiente').exclude(id=solicitud_id).update(estado='rechazada')
                    messages.info(request, 'Se ha ocupado el ultimo cupo disponible, ahora las solicitudes restantes estaran rechazadas')
                    return HttpResponseRedirect(url)
                else:
                    messages.success(request, f'Solicitud aceptada exitosamente.')
            else:
                messages.error(request, f'No hay más cupos disponibles.')

            proyecto.save()
            send_mail('¡Solicitud Aceptada!', 'Tu solicitud ha sido aceptada, por lo tanto, puedes participar en este proyecto!', 'cuentaprueba4326@gmail.com', [solicitud.miembro.email])
    
        elif decision == 'rechazar':
            solicitud.estado = 'rechazada'
            send_mail('¡Solicitud Rechazada!', 'Tu solicitud ha sido rechazada, por lo tanto, no puedes participar en este proyecto!', 'cuentaprueba4326@gmail.com', [solicitud.miembro.email])

        solicitud.save()


    if 'q' in request.GET:
        q = request.GET['q'].lower()
        solicitudes_pendientes = Solicitud.objects.filter(
            Q(proyecto__nombre_proyecto__iexact=q) | Q(miembro__rut__iexact=q) | Q(miembro__first_name__iexact=q) | Q(miembro__last_name__iexact=q), 
            estado = 'pendiente').order_by('-fecha_solicitud')
        paginator = Paginator(solicitudes_pendientes, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        solicitudes_pendientes = Solicitud.objects.filter(estado = 'pendiente').order_by('-fecha_solicitud')
        paginator = Paginator(solicitudes_pendientes, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    return render(request, 'proyectos/gestionar_solicitudes.html', {
        'solicitudes_pendientes': solicitudes_pendientes,
        'page_obj': page_obj,
    })


@staff_member_required
def gestionar_solicitudes_aceptada(request):
    if 'q' in request.GET:
        q = request.GET['q'].lower()
        solicitudes_aceptadas = Solicitud.objects.filter(
            Q(proyecto__nombre_proyecto__iexact=q) | Q(miembro__rut__iexact=q) | Q(miembro__first_name__iexact=q) | Q(miembro__last_name__iexact=q), 
            estado = 'aceptada').order_by('-fecha_solicitud')
        paginator = Paginator(solicitudes_aceptadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        solicitudes_aceptadas = Solicitud.objects.filter(estado = 'aceptada').order_by('-fecha_solicitud')
        paginator = Paginator(solicitudes_aceptadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    return render(request, 'proyectos/gestionar_solicitudes_aceptada.html', {
        'solicitudes_aceptadas': solicitudes_aceptadas,
        'page_obj': page_obj,
    })

@staff_member_required
def gestionar_solicitudes_rechazada(request):
    if 'q' in request.GET:
        q = request.GET['q'].lower()
        solicitudes_rechazadas = Solicitud.objects.filter(
            Q(proyecto__nombre_proyecto__iexact=q) | Q(miembro__rut__iexact=q) | Q(miembro__first_name__iexact=q) | Q(miembro__last_name__iexact=q), 
            estado = 'rechazada').order_by('-fecha_solicitud')
        paginator = Paginator(solicitudes_rechazadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        solicitudes_rechazadas = Solicitud.objects.filter(estado = 'rechazada').order_by('-fecha_solicitud')
        paginator = Paginator(solicitudes_rechazadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    return render(request, 'proyectos/gestionar_solicitudes_rechazada.html', {
        'solicitudes_rechazadas': solicitudes_rechazadas,
        'page_obj': page_obj,
    })

# -----------------------------------------------------------------------------

# Vista para que el usuario miembro pueda ver sus solicitudes pendientes
@login_required
def mis_solicitudes(request):
    if 'q' in request.GET:
        usuario = request.user
        q = request.GET['q'].lower()
        solicitudes_pendientes = Solicitud.objects.filter(
            Q(proyecto__nombre_proyecto__iexact=q) | 
            Q(miembro__rut__iexact=q) | 
            Q(miembro__first_name__iexact=q) | 
            Q(miembro__last_name__iexact=q), 
            estado = 'pendiente', miembro__rut=usuario).order_by('-fecha_solicitud')
       
    else:
        usuario = request.user
        solicitudes_pendientes = Solicitud.objects.filter(estado = 'pendiente', miembro__rut=usuario).order_by('-fecha_solicitud')

    paginator = Paginator(solicitudes_pendientes, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'proyectos/mis_solicitudes.html', {
        # 'solicitudes': solicitudes,
        # 'solicitudes_pendientes': solicitudes_pendientes,
        'page_obj': page_obj,
    })


# Vista para que el usuario miembro peuda ver sus solicitudes aceptadas
@login_required
def mis_solicitudes_aceptada(request):
    if 'q' in request.GET:
        usuario = request.user
        q = request.GET['q'].lower()
        solicitudes_aceptadas = Solicitud.objects.filter(
            Q(proyecto__nombre_proyecto__iexact=q) | 
            Q(miembro__rut__iexact=q) | 
            Q(miembro__first_name__iexact=q) | 
            Q(miembro__last_name__iexact=q), 
            estado = 'aceptada', miembro__rut=usuario).order_by('-fecha_solicitud')
        
    else:
        usuario = request.user
        solicitudes_aceptadas = Solicitud.objects.filter(estado = 'aceptada', miembro__rut=usuario).order_by('-fecha_solicitud')

    paginator = Paginator(solicitudes_aceptadas, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'proyectos/mis_solicitudes_aceptada.html', {
        # 'solicitudes': solicitudes,
        # 'solicitudes_aceptadas': solicitudes_aceptadas,
        'page_obj': page_obj,
    })


# Vista para que el usuario miembro pueda ver sus solicitudes rechazadas
@login_required
def mis_solicitudes_rechazada(request):
    if 'q' in request.GET:
        usuario = request.user
        q = request.GET['q'].lower()
        solicitudes_rechazadas = Solicitud.objects.filter(
            Q(proyecto__nombre_proyecto__iexact=q) | Q(miembro__rut__iexact=q) | Q(miembro__first_name__iexact=q) | Q(miembro__last_name__iexact=q), 
            estado = 'rechazada', miembro__rut=usuario).order_by('-fecha_solicitud')
        paginator = Paginator(solicitudes_rechazadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        usuario = request.user
        solicitudes_rechazadas = Solicitud.objects.filter(estado = 'rechazada', miembro__rut=usuario).order_by('-fecha_solicitud')
        paginator = Paginator(solicitudes_rechazadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    return render(request, 'proyectos/mis_solicitudes_rechazada.html', {
        # 'solicitudes': solicitudes,
        # 'solicitudes_rechazadas': solicitudes_rechazadas,
        'page_obj': page_obj,
    })


# -------------------------------------------------------------------------------------------------------------------------------------------------------------

def carouselProyectos(request, pk):
     # Renderizar el template correspondiente y pasar la URL de la imagen
    imagen = get_object_or_404(Carousel, pk=pk)
    template = "proyectos/carouselProyectos.html"

    return render(request, template, {'imagen': imagen})