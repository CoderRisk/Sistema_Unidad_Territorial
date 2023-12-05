from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto, Solicitud, SolicitudArchivo
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
import re

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

            inicio_postulacion = form.cleaned_data['inicio_postulacion']
            cierre_postulacion = form.cleaned_data['cierre_postulacion']
            proyecto_en_marcha = form.cleaned_data['inicio_del_proyecto']
            proyecto_fin_marcha = form.cleaned_data['fin_del_proyecto']

            # Validación personalizada para asegurarse de que la fecha de inicio sea anterior a la fecha de término
            if inicio_postulacion > cierre_postulacion:
                form.add_error('inicio_postulacion', 'La fecha de inicio de postulación debe ser menor a la fecha de cierre de postulación.')

            if cierre_postulacion < inicio_postulacion:
                form.add_error('cierre_postulacion', 'La fecha de cierre de postulación debe ser menor a la fecha de inicio de postulación.')

            if proyecto_en_marcha < cierre_postulacion.date():
                form.add_error('inicio_del_proyecto', 'La fecha de inicio del proyecto debe ser después a la fecha de cierre de postulación.')

            if proyecto_en_marcha == cierre_postulacion.date():
                form.add_error('inicio_del_proyecto', 'La fecha del proyecto no puede ser igual al cierre de postulación.')
            
            if proyecto_fin_marcha < proyecto_en_marcha:
                form.add_error('fin_del_proyecto', 'La fecha fin del proyecto debe ser mayor a la fecha de inicio del proyecto.')

            # Otras validaciones personalizadas aquí...

            if form.errors:
                # Si hay errores, renderiza nuevamente el formulario con los errores personalizados.
                return render(request, 'proyectos/crear_proyecto.html', {'form': form})

            # Resto del código...

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
        if form.is_valid():
            
            inicio_postulacion = form.cleaned_data['inicio_postulacion']
            cierre_postulacion = form.cleaned_data['cierre_postulacion']
            proyecto_en_marcha = form.cleaned_data['inicio_del_proyecto']
            proyecto_fin_marcha = form.cleaned_data['fin_del_proyecto']

            # Validación personalizada para asegurarse de que la fecha de inicio sea anterior a la fecha de término
            if inicio_postulacion > cierre_postulacion:
                form.add_error('inicio_postulacion', 'La fecha de inicio debe ser menor a la fecha de término.')

            if cierre_postulacion < inicio_postulacion:
                form.add_error('cierre_postulacion', 'La fecha de término debe ser menor a la fecha de inicio.')

            if proyecto_en_marcha < cierre_postulacion.date():
                form.add_error('inicio_del_proyecto', 'La fecha del proyecto debe ser mayor a la postulación.')

            if proyecto_en_marcha == cierre_postulacion.date():
                form.add_error('inicio_del_proyecto', 'La fecha del proyecto no puede ser igual a la postulación.')
            
            if proyecto_fin_marcha < proyecto_en_marcha:
                form.add_error('fin_del_proyecto', 'La fecha fin del proyecto debe ser mayor a la fecha de inicio del proyecto.')

            # Otras validaciones personalizadas aquí...

            if form.errors:
                # Si hay errores, renderiza nuevamente el formulario con los errores personalizados.
                return render(request, 'proyectos/editar_proyecto.html', {'form': form, 'proyectos': proyectos})

            # Actualiza el campo en el modelo
            proyectos.inicio_postulacion = inicio_postulacion
            proyectos.cierre_postulacion = cierre_postulacion

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
            form = PostulacionForm(request.POST, request.FILES)
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

                    archivos_adjuntos = request.FILES.getlist('archivos_adjuntos')

                    for archivo in archivos_adjuntos:
                        SolicitudArchivo.objects.create(campo_solicitud=solicitud, archivo=archivo)


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
            send_mail('¡Solicitud Aceptada!', 
                       f'Hola {request.user.first_name} tu solicitud ha sido aceptada, actualmente has postulado a: {proyecto.nombre_proyecto}\n\n'
                      f'¡Muchas Gracias!\n\n'
                      f'Este mensaje es generado automáticamente; le agradecemos que no responda al mismo.\n\n'
                      f'SORTE', 
                      'cuentaprueba4326@gmail.com', [solicitud.miembro.email])
    
        elif decision == 'rechazar':
            solicitud.estado = 'rechazada'
            messages.success(request, f'La Solicitud ha sido rechazada.')
            send_mail('¡Solicitud Rechazada!', 
                      f'Hola {request.user.first_name} tu solicitud ha sido rechazada, por lo tanto, no puedes participar en nuestro proyecto: {solicitud.proyecto.nombre_proyecto}\n\n' 
                      f'Por favor, no dude en ponerse en contacto con nuestro equipo de soporte ante cualquier situación que considere necesaria.\n\n'
                      f'Este mensaje es generado automáticamente; le agradecemos que no responda al mismo.\n\n'
                      f'SORTE\n\n', 
                      'cuentaprueba4326@gmail.com', 
                      [solicitud.miembro.email])

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
def gestionar_solicitudes_ver(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud_archivo = SolicitudArchivo.objects.filter(campo_solicitud=solicitud)

    archivos_solicitud = []
    for archivo_adjunto in solicitud_archivo:
        # Obtener el nombre del archivo después de la segunda barra
        nombre_archivo = archivo_adjunto.archivo.name.split("/", 2)[-1]
        archivos_solicitud.append({
            'archivo_adjunto': archivo_adjunto,
            'nombre_archivo': nombre_archivo,
        })

    return render(request, 'proyectos/gestionar_solicitudes_ver.html', {
        'solicitud': solicitud,
        'archivos_solicitud': archivos_solicitud,
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