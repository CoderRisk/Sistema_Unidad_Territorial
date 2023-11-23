from django.shortcuts import render, get_object_or_404, redirect
from .models import Actividad, Inscripcion
from .forms import ActividadForm, InscripcionForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView
from core.models import Carousel
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

# ----------------------------------------------------------------------

# Listar actividades
def listar_actividad(request):
    imagenes = Carousel.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        actividades = Actividad.objects.filter(
            Q(nombre_actividad__icontains=q) | 
            Q(descripcion__icontains=q)).order_by('-fecha_creacion_actividad')
        paginator = Paginator(actividades, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        actividades = Actividad.objects.all().order_by('-fecha_creacion_actividad')
        paginator = Paginator(actividades, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    return render(request, "actividades/listar_actividad.html", {
        'page_obj': page_obj,
        'imagenes': imagenes
    })

# ----------------------------------------------------------------------

# Detalle de actividad
def detalle_actividad(request, pk):
    actividades = get_object_or_404(Actividad, pk=pk)
    return render(request, 'actividades/detalle_actividad.html', {'actividades': actividades})

# ----------------------------------------------------------------------

# Crear actividad
@staff_member_required
def crear_actividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST, request.FILES)
        if form.is_valid():
            actividad = form.save(commit=False)

            fecha_actividad = form.cleaned_data['fecha_actividad']
            hora_inicio = form.cleaned_data['hora_inicio']
            fecha_actividad_tiempo_inicio = datetime.combine(fecha_actividad, hora_inicio)

            hora_termino = form.cleaned_data['hora_termino']
            fecha_actividad_tiempo_termino = datetime.combine(fecha_actividad, hora_termino)

            if hora_inicio >= hora_termino:
                form.add_error('hora_inicio', 'La hora de inicio debe ser menor a la hora de término.')
             
            
            if hora_termino <= hora_inicio:
                form.add_error('hora_termino', 'La hora de término debe ser mayor a la hora de inicio.')
              
            if form.errors:
                # Si hay errores, renderiza nuevamente el formulario con los errores personalizados.
                return render(request, 'actividades/crear_actividad.html', {'form': form})

            actividad.fecha_actividad_tiempo_inicio = fecha_actividad_tiempo_inicio
            actividad.fecha_actividad_tiempo_termino = fecha_actividad_tiempo_termino

            actividad.save()

            messages.success(request, '¡La actividad ha sido creada con éxito!')
            return redirect('listar_actividad')
        else:
            print(form)
    else:
        form = ActividadForm()
    return render(request, 'actividades/crear_actividad.html', {'form': form})

# ---------------------------------------------------------------------

# Editar actividad
@staff_member_required
def editar_actividad(request, pk):
    actividades = get_object_or_404(Actividad, pk=pk)
    if request.method == 'POST':
        form = ActividadForm(request.POST, request.FILES, instance=actividades)
        if form.is_valid():

            # Combina fecha y hora antes de guardar en el modelo
            fecha_inicio = form.cleaned_data['fecha_actividad']
            fecha_inicio_hora = form.cleaned_data['hora_inicio']
            fecha_tiempo_inicio = datetime.combine(fecha_inicio, fecha_inicio_hora)

            fecha_termino = form.cleaned_data['fecha_actividad']
            fecha_termino_hora = form.cleaned_data['hora_termino']
            fecha_date_termino = datetime.combine(fecha_termino, fecha_termino_hora)

            if fecha_inicio_hora >= fecha_termino_hora:
                form.add_error('hora_inicio', 'La hora de inicio debe ser menor a la hora de término.')
             
            
            if fecha_termino_hora <= fecha_inicio_hora:
                form.add_error('hora_termino', 'La hora de término debe ser mayor a la hora de inicio.')
              
            if form.errors:
                # Si hay errores, renderiza nuevamente el formulario con los errores personalizados.
                return render(request, 'actividades/editar_actividad.html', {'form': form, 'actividades': actividades})

            # Actualiza el campo en el modelo
            actividades.fecha_actividad_tiempo_inicio = fecha_tiempo_inicio
            actividades.fecha_actividad_tiempo_termino = fecha_date_termino

            form.save()

            actividad = actividades.fecha_creacion_actividad

            messages.success(request, '¡La actividad ha sido editada con éxito!')
            return redirect('listar_actividad')
        else:
            # Acceder a los datos limpios de un campo específico
            hora_inicio = form.data.get('hora_inicio')
            hora_termino = form.data.get('hora_termino')

            if hora_inicio and hora_termino and hora_inicio > hora_termino:
                # Agregar un error al campo hora_inicio
                form.add_error('hora_inicio', 'La hora de inicio no puede ser posterior a la hora de término.')

            if hora_inicio and hora_termino and hora_termino < hora_inicio:
                # Agregar un error al campo hora_inicio
                form.add_error('hora_termino', 'La hora de término no puede ser anterior a la hora de inicio.')
    else:
        form = ActividadForm(instance=actividades)
    return render(request, 'actividades/editar_actividad.html', {'form': form, 'actividades': actividades})

# --------------------------------------------------------------------

# Eliminar actividad
@staff_member_required
def eliminar_actividad(request, pk):
    actividades = get_object_or_404(Actividad, pk=pk)
    if request.method == 'POST':
        actividades.delete()
        messages.success(request, '¡La Actividad ha sido eliminada correctamente!')
        return redirect('listar_actividad')
    return render(request, 'actividades/eliminar_actividad_confirmar.html', {'actividades': actividades})

# ---------------------------------------------------------------------------------------------------------------------------

# Vista para la inscripción de actividades
@login_required
def inscribir_actividad(request, actividad_id):
    actividad = Actividad.objects.get(id=actividad_id)

    if actividad.cupos_disponibles > 0:
        if request.method == 'POST':
            form = InscripcionForm(request.POST)
            if form.is_valid():
                inscripcion = form.save(commit=False)
                inscripcion.actividad = actividad
                inscripcion.miembro = request.user
                inscripcion.estado = 'pendiente'
                

                # Verifica si el usuario ya ha postulado a la actividad
                inscripcion_existente = Inscripcion.objects.filter(actividad=actividad, miembro=request.user).first()

                if inscripcion_existente is not None:
                    messages.error(request, 'Lo sentimos, pero ya has enviado una solicitud para esta actividad')
                else:
                    inscripcion.save()
                    inscripcion.fecha_solicitud = datetime.now()
                    
                    
                    actividad.save()

                    fecha_actual = datetime.now().strftime("%d-%m-%Y")
                    hora_actual = datetime.now().strftime("%H:%M:%S")

                    messages.success(request, 'Tu solicitud ha sido enviada y será gestionada por nuestra directiva.')
                    send_mail(
                        'Confirmación de Inscripción',
                        f'Hola {request.user.first_name} {request.user.last_name},\n\n'
                        f'Con fecha {fecha_actual} y hora {hora_actual} te informamos que tu solicitud '
                        f'a la actividad {actividad.nombre_actividad} ha sido recibida y será gestionada por nuestra directiva. '
                        f'Te confirmaremos si fue aceptada o rechazada por correo.\n\n¡Muchas Gracias!\n\nSORTE',
                        'cuentaprueba4326@gmail.com',
                        [request.user.email]
                    )
                    return redirect('mis_solicitudes_miembro')
        else:
            form = InscripcionForm(initial={'nombre': request.user.first_name, 'apellido': request.user.last_name})

        return render(request, 'actividades/inscribir_actividad.html', {'form': form, 'actividad': actividad})
    else:
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.now().strftime("%H:%M:%S")
        messages.error(request, 'Lo sentimos, pero ya no hay cupos disponibles para esta actividad.')
        send_mail(
            'Cupos Agotados',
            f'Hola {request.user.first_name} {request.user.last_name},\n\nCon fecha {fecha_actual} y hora {hora_actual} damos respuesta a tu solicitud para '
            f'comunicarte que la actividad con nombre {actividad.nombre_actividad} no tiene cupos disponibles.\n\nLamentamos los inconvenientes\n\nSORTE',
            'cuentaprueba4326@gmail.com',
            [request.user.email]
        )
        return redirect('listar_actividad')

# ---------------------------------------------------------------------------------------------------------------------------

# Vista para la gestión de inscripciones a las actividades por parte del admin
@staff_member_required
def gestionar_inscripciones(request):
    if not request.user.is_staff:
        return redirect('inicio')

    # inscripciones = Inscripcion.objects.all()

    if request.method == 'POST':
        inscripcion_id = request.POST.get('inscripcion_id')
        decision = request.POST.get('decision')
        inscripcion = Inscripcion.objects.get(id=inscripcion_id)
        nombre_actividad = inscripcion.actividad.nombre_actividad

        if decision == 'aceptar':
            inscripcion.estado = 'aceptada'
            actividad = inscripcion.actividad

            if actividad.cupos_disponibles > 0:
                actividad.cupos_disponibles -= 1

                if actividad.cupos_disponibles == 0:
                    # Obtener la URL inversa basada en el nombre del patrón de URL
                    url = reverse('gestionar_inscripciones')
                    inscripcion.save()
                    actividad.save()
                    Inscripcion.objects.filter(actividad=actividad, estado='pendiente').exclude(id=inscripcion_id).update(estado='rechazada')
                    messages.info(request, 'Se ha ocupado el ultimo cupo disponible, ahora las solicitudes restantes estaran rechazadas')
                    return HttpResponseRedirect(url)
                else:
                    messages.success(request, f'Solicitud aceptada exitosamente.')
            else:
                Inscripcion.objects.filter(actividad=actividad, estado='pendiente').exclude(id=inscripcion_id).update(estado='rechazada')
                messages.error(request, f'No hay más cupos disponibles.')

                # Puedes usarla aquí o asignarla a None si no hay actividad
                cupos_agotados = actividad.cupos_disponibles <= 0 if actividad else None

            actividad.save()
            send_mail('Inscripción Aceptada', 'Tu Inscripción ha sido aceptada, por lo tanto, puedes participar en nuestra actividad!', 'cuentaprueba4326@gmail.com', [inscripcion.miembro.email])
        
        elif decision == 'rechazar':

            inscripcion.estado = 'rechazada'
            send_mail('Inscripción Rechazada', 'Tu Inscripción ha sido rechazada, por lo tanto, no puedes participar en nuestra actividad!', 'cuentaprueba4326@gmail.com', [inscripcion.miembro.email])

        inscripcion.save()

    if 'q' in request.GET:
        q = request.GET['q'].lower()
        inscripciones_pendientes = Inscripcion.objects.filter(
            Q(actividad__nombre_actividad__iexact=q) | Q(miembro__rut__iexact=q) | Q(miembro__first_name__iexact=q) | Q(miembro__last_name__iexact=q), 
            estado = 'pendiente').order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_pendientes, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        cupos_agotados = None  # Si no hay solicitud, la variable cupos_agotados se inicializa como None
        inscripciones_pendientes = Inscripcion.objects.filter(estado='pendiente').order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_pendientes, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    return render(request, 'actividades/gestionar_inscripciones.html', {
        'page_obj': page_obj,
        'cupos_agotados': cupos_agotados,
    })


# Vista para las inscripciones aceptadas de las actividades por parte del admin
@staff_member_required
def gestionar_inscripciones_aceptadas(request):
    if 'q' in request.GET:
        q = request.GET['q'].lower()
        inscripciones_aceptadas = Inscripcion.objects.filter(
            Q(actividad__nombre_actividad__iexact=q) | Q(miembro__rut__iexact=q) | Q(miembro__first_name__iexact=q) | Q(miembro__last_name__iexact=q), 
            estado = 'aceptada').order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_aceptadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        inscripciones_aceptadas = Inscripcion.objects.filter(estado='aceptada').order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_aceptadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    return render(request, 'actividades/gestionar_inscripciones_aceptada.html',{
        'page_obj': page_obj,
    })


@staff_member_required
def gestionar_inscripciones_rechazadas(request):
    if 'q' in request.GET:
        q = request.GET['q'].lower()
        inscripciones_rechazadas = Inscripcion.objects.filter(
            Q(actividad__nombre_actividad__iexact=q) | Q(miembro__rut__iexact=q) | Q(miembro__first_name__iexact=q) | Q(miembro__last_name__iexact=q), 
            estado = 'rechazada').order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_rechazadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        inscripciones_rechazadas = Inscripcion.objects.filter(estado='rechazada').order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_rechazadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    return render(request, 'actividades/gestionar_inscripciones_rechazada.html',{
        'page_obj': page_obj,
    })

# --------------------------------------------------------------------------------------------------------------------------------

# Vista para que el usuario miembro pueda ver sus solicitudes pendientes
@login_required
def mis_solicitudes_miembro(request):

    if 'q' in request.GET:
        usuario =  request.user
        q = request.GET['q'].lower()
        inscripciones_pendientes = Inscripcion.objects.filter(
            Q(actividad__nombre_actividad__iexact=q) | Q(miembro__rut__iexact=q) | Q(miembro__first_name__iexact=q) | Q(miembro__last_name__iexact=q), 
            estado = 'pendiente', miembro__rut=usuario).order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_pendientes, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        usuario =  request.user
        inscripciones_pendientes = Inscripcion.objects.filter(estado='pendiente', miembro__rut=usuario).order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_pendientes, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    return render(request, 'actividades/mis_solicitudes_miembro.html', {
        'inscripciones_pendientes': inscripciones_pendientes,
        "page_obj": page_obj,
    })


# Vista para que el usuario miembro peuda ver sus solicitudes aceptadas
@login_required
def mis_solicitudes_miembro_aceptada(request):
    if 'q' in request.GET:
        usuario =  request.user
        q = request.GET['q'].lower()
        inscripciones_aceptadas = Inscripcion.objects.filter(
            Q(actividad__nombre_actividad__iexact=q) | Q(miembro__rut__iexact=q) | Q(miembro__first_name__iexact=q) | Q(miembro__last_name__iexact=q), 
            estado = 'aceptada', miembro__rut=usuario).order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_aceptadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        usuario =  request.user
        inscripciones_aceptadas = Inscripcion.objects.filter(estado='aceptada', miembro__rut=usuario).order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_aceptadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    return render(request, 'actividades/mis_solicitudes_miembro_aceptada.html', {
        'inscripciones_aceptadas': inscripciones_aceptadas,
        'page_obj': page_obj,
    })


# Vista para que el usuario miembro pueda ver sus solicitudes rechazadas
@login_required
def mis_solicitudes_miembro_rechazada(request):
    if 'q' in request.GET:
        usuario =  request.user
        q = request.GET['q'].lower()
        inscripciones_rechazadas = Inscripcion.objects.filter(
            Q(actividad__nombre_actividad__iexact=q) | Q(miembro__rut__iexact=q) | Q(miembro__first_name__iexact=q) | Q(miembro__last_name__iexact=q), 
            estado = 'rechazada', miembro__rut=usuario).order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_rechazadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        usuario =  request.user
        inscripciones_rechazadas = Inscripcion.objects.filter(estado='rechazada', miembro__rut=usuario).order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_rechazadas, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    return render(request, 'actividades/mis_solicitudes_miembro_rechazada.html', {
        # 'inscripciones': inscripciones,
        'inscripciones_rechazadas': inscripciones_rechazadas,
        'page_obj': page_obj,
    })
# --------------------------------------------------------------------------------------------------------------------------------


def carouselActividades(request, pk):
     # Renderizar el template correspondiente y pasar la URL de la imagen
    imagen = get_object_or_404(Carousel, pk=pk)
    template = "actividades/carouselActividades.html"

    return render(request, template, {'imagen': imagen})