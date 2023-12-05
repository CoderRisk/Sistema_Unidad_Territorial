from django.shortcuts import render, get_object_or_404, redirect
from .models import Actividad, Inscripcion, SolicitudInscripcion
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

            inicio_inscripcion = form.cleaned_data['inicio_inscripcion']
            cierre_inscripcion = form.cleaned_data['cierre_inscripcion']
            inicio_actividad = form.cleaned_data['inicio_actividad']
            fin_actividad = form.cleaned_data['fin_actividad']

            if inicio_inscripcion >= cierre_inscripcion:
                form.add_error('inicio_inscripcion', 'La fecha de inicio de inscripción debe ser menor a la fecha de cierre de inscripción.')
            
            if cierre_inscripcion <= inicio_inscripcion:
                form.add_error('cierre_inscripcion', 'La fecha de cierre de inscripción debe ser mayor a la fecha de inicio de inscripción.')

            if inicio_actividad <= cierre_inscripcion.date():
                form.add_error('inicio_actividad', 'La fecha de inicio de actividad debe ser mayor a la fecha de cierre de inscripción.')

            if fin_actividad <= inicio_actividad:
                form.add_error('fin_actividad', 'La fecha del fin de la actividad debe ser mayor a la fecha de inicio de actividad.')

            if form.errors:
                # Si hay errores, renderiza nuevamente el formulario con los errores personalizados.
                return render(request, 'actividades/crear_actividad.html', {'form': form})

            actividad.inicio_inscripcion = inicio_inscripcion
            actividad.cierre_inscripcion = cierre_inscripcion

            actividad.save()

            messages.success(request, '¡La actividad ha sido creada con éxito!')
            return redirect('listar_actividad')
  
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

            inicio_inscripcion = form.cleaned_data['inicio_inscripcion']
            cierre_inscripcion = form.cleaned_data['cierre_inscripcion']
            inicio_actividad = form.cleaned_data['inicio_actividad']
            fin_actividad = form.cleaned_data['fin_actividad']

            if inicio_inscripcion >= cierre_inscripcion:
                form.add_error('inicio_inscripcion', 'La fecha de inicio de inscripción debe ser menor a la fecha de cierre de inscripción.')
            
            if cierre_inscripcion <= inicio_inscripcion:
                form.add_error('cierre_inscripcion', 'La fecha de cierre de inscripción debe ser mayor a la fecha de inicio de inscripción.')

            if inicio_actividad <= cierre_inscripcion.date():
                form.add_error('inicio_actividad', 'La fecha de inicio de actividad debe ser mayor a la fecha de cierre de inscripción.')

            if fin_actividad <= inicio_actividad:
                form.add_error('fin_actividad', 'La fecha del fin de la actividad debe ser mayor a la fecha de inicio de actividad.')

            if form.errors:
                # Si hay errores, renderiza nuevamente el formulario con los errores personalizados.
                return render(request, 'actividades/editar_actividad.html', {'form': form, 'actividades': actividades})

            # Actualiza el campo en el modelo
            actividades.inicio_inscripcion = inicio_inscripcion
            actividades.cierre_inscripcion = cierre_inscripcion

            form.save()

            # actividad = actividades.fecha_creacion_actividad

            messages.success(request, '¡La actividad ha sido editada con éxito!')
            return redirect('listar_actividad')
      

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
            print(form.errors)
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

                    archivos_adjuntos = request.FILES.getlist('archivos_adjuntos')

                    if archivos_adjuntos:
                        for archivo in archivos_adjuntos:
                            SolicitudInscripcion.objects.create(campo_inscripcion=inscripcion, archivo=archivo)
                        
                    
                    
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
                    messages.info(request, 'Se ha ocupado el ultimo cupo disponible, ahora las solicitudes restantes estarán rechazadas')
                    return HttpResponseRedirect(url)
                else:
                    messages.success(request, f'Solicitud aceptada exitosamente.')
            else:
                Inscripcion.objects.filter(actividad=actividad, estado='pendiente').exclude(id=inscripcion_id).update(estado='rechazada')
                messages.error(request, f'No hay más cupos disponibles.')

                # Puedes usarla aquí o asignarla a None si no hay actividad
                cupos_agotados = actividad.cupos_disponibles <= 0 if actividad else None

            actividad.save()
            # 'Confirmación de Inscripción',
            # f'Hola {request.user.first_name} {request.user.last_name},\n\n'
            # f'Con fecha {fecha_actual} y hora {hora_actual} te informamos que tu solicitud '
            # f'a la actividad {actividad.nombre_actividad} ha sido recibida y será gestionada por nuestra directiva. '
            # f'Te confirmaremos si fue aceptada o rechazada por correo.\n\n¡Muchas Gracias!\n\nSORTE',
            # 'cuentaprueba4326@gmail.com',
            # [request.user.email]
            send_mail('Inscripción Aceptada', 
                      f'Hola {request.user.first_name} tu inscripción ha sido aceptada, actualmente estas inscrito a: {actividad.nombre_actividad} \n\n'
                      f'¡Muchas Gracias!\n\n'
                      f'Este mensaje es generado automáticamente; le agradecemos que no responda al mismo.\n\n'
                      f'SORTE',
                      'cuentaprueba4326@gmail.com', 
                      [inscripcion.miembro.email])
        
        elif decision == 'rechazar':

            inscripcion.estado = 'rechazada'
            messages.success(request, f'La solicitud ha sido rechazada.')
            send_mail('Inscripción Rechazada', 
                      f'Hola {request.user.first_name} tu inscripción ha sido rechazada, por lo tanto, no puedes participar en nuestra actividad: {inscripcion.actividad.nombre_actividad}\n\n' 
                      f'Por favor, no dude en ponerse en contacto con nuestro equipo de soporte ante cualquier situación que considere necesaria.\n\n'
                      f'Este mensaje es generado automáticamente; le agradecemos que no responda al mismo.\n\n'
                      f'SORTE\n\n',
                      'cuentaprueba4326@gmail.com', 
                      [inscripcion.miembro.email])

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
        inscripciones_pendientes = Inscripcion.objects.filter(estado='pendiente').order_by('-fecha_solicitud')
        paginator = Paginator(inscripciones_pendientes, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    return render(request, 'actividades/gestionar_inscripciones.html', {
        'page_obj': page_obj,
    })

@staff_member_required
def gestionar_inscripciones_ver(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    inscripcion_archivo = SolicitudInscripcion.objects.filter(campo_inscripcion=inscripcion)
    print(inscripcion)

    archivos_solicitud = []
    if inscripcion_archivo:
        for archivo_adjunto in inscripcion_archivo:
            # Obtener el nombre del archivo después de la segunda barra
            nombre_archivo = archivo_adjunto.archivo.name.split("/", 2)[-1]
            archivos_solicitud.append({
                'archivo_adjunto': archivo_adjunto,
                'nombre_archivo': nombre_archivo,
            })


    return render(request, 'actividades/gestionar_inscripciones_ver.html', {
        'inscripcion': inscripcion,
        'archivos_solicitud': archivos_solicitud,
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