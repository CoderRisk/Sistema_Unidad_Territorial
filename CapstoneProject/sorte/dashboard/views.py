from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, HttpResponse
from users.models import CustomUSer
import base64
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
plt.matplotlib.use('Agg')
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from actividades.models import Actividad
from proyectos.models import Proyecto
from django.db import models
import numpy as np
import matplotlib.dates as mdates
from proyectos.models import Solicitud
from collections import Counter
from actividades.models import Inscripcion



# Create your views here.
def inicioDashboard(request):
    return render(request, 'dashboard/inicio.html',)


@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    # Datos de la distribución de género
    genero_counts = CustomUSer.objects.filter(gender__isnull=False).values('gender').annotate(total=Count('gender'))
    labels = [entry['gender'] for entry in genero_counts]
    data = [entry['total'] for entry in genero_counts]

    # Colores personalizados para cada categoría
    colors = ['lightcoral', 'lightskyblue', 'lightgreen', 'lightpink']

    # Crear el gráfico de torta
    fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
    ax_pie.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops=dict(width=0.4), textprops={'color':"w", 'fontsize': 18, 'weight': 700})
    ax_pie.legend(labels, title="Género", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize='medium')
    ax_pie.axis('equal')
    fig_pie.set_facecolor('#033076')

    # Guardar el gráfico de torta en BytesIO
    with BytesIO() as image_stream_pie:
        plt.savefig(image_stream_pie, format='png', bbox_inches='tight')
        image_stream_pie.seek(0)
        image_base64_pie = base64.b64encode(image_stream_pie.getvalue()).decode('utf-8')

    # Crear el gráfico de barras con números enteros en el eje y
    fig_bar, ax_bar = plt.subplots(figsize=(8, 6))
    ax_bar.bar(labels, data, color=colors)
    # Colorear el fondo del gráfico de barras
    ax_bar.set_facecolor('#033076')
    ax_bar.set_xlabel('Género')
    ax_bar.set_ylabel('Número de Usuarios')

    # Formatear el eje y como números enteros
    ax_bar.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    ax_bar.set_ylim(0, 10)  # Cambiando el rango de valores del eje Y

    # Guardar el gráfico de barras en BytesIO
    with BytesIO() as image_stream_bar:
        plt.savefig(image_stream_bar, format='png', bbox_inches='tight')
        image_stream_bar.seek(0)
        image_base64_bar = base64.b64encode(image_stream_bar.getvalue()).decode('utf-8')

    # Datos para el gráfico de dispersión (edad vs. cantidad de usuarios)
    usuario_birthdate_counts = CustomUSer.objects.filter(birthdate__isnull=False).values('birthdate').annotate(count=Count('birthdate'))

    # Extraer las fechas de nacimiento y los conteos
    birthdates = [entry['birthdate'] for entry in usuario_birthdate_counts]
    usuario_counts = [entry['count'] for entry in usuario_birthdate_counts]

    # Crear el gráfico de dispersión
    fig_scatter, ax_scatter = plt.subplots(figsize=(8, 6))
    ax_scatter.scatter(birthdates, usuario_counts)
    # Colorear el fondo del gráfico de dispersión
    ax_scatter.set_facecolor('#033076')
    ax_scatter.set_xlabel('Año de nacimiento de los Usuarios')
    ax_scatter.set_ylabel('Cantidad de Usuarios')

    # Formatear el eje Y como números enteros
    ax_scatter.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    
    # Ajustar el rango de valores del eje Y
    ax_scatter.set_ylim(0, 10)

    # Guardar el gráfico de dispersión en BytesIO
    with BytesIO() as image_stream_scatter:
        plt.savefig(image_stream_scatter, format='png', bbox_inches='tight')
        image_stream_scatter.seek(0)
        image_base64_scatter = base64.b64encode(image_stream_scatter.getvalue()).decode('utf-8')

    # Convertir los datos a un DataFrame de pandas
    data_dict = {'Género': labels, 'Número de Usuarios': data}
    df = pd.DataFrame(data_dict)

    data_dict2 = {'Año de Nacimiento': birthdates, 'Número de Usuarios': usuario_counts}
    df2 = pd.DataFrame(data_dict2)

    # Guardar el DataFrame como un archivo Excel
    excel_file_path = 'datos.xlsx'
    df.to_excel(excel_file_path, index=False)

    excel_file_path2 = 'datosNacimientoUsuarios.xlsx'
    df2.to_excel(excel_file_path2, index=False)

    # Renderizar la plantilla con los gráficos y el enlace de descarga
    return render(
        request,
        'dashboard/dashboard.html',
        {
            'image_base64_pie': image_base64_pie,
            'image_base64_bar': image_base64_bar,
            'image_base64_scatter': image_base64_scatter,
            'excel_file_path': excel_file_path, 
            'excel_file_path2': excel_file_path2,
        }
    )


@user_passes_test(lambda u: u.is_staff)
def dashboard_actividad(request):
    # Obtener datos para el gráfico de barras por comuna
    actividades_por_comuna = Actividad.objects.values('comuna').annotate(total=Count('id'))

    # Crear el gráfico de barras por comuna
    comunas = [actividad['comuna'] for actividad in actividades_por_comuna]
    cantidades_actividades_comuna = [actividad['total'] for actividad in actividades_por_comuna]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(comunas, cantidades_actividades_comuna, color='skyblue')
    ax.set_xlabel('Comuna')
    ax.set_ylabel('Cantidad de Actividades')
    ax.set_title('Gráfico de Barras (Comuna)')
    plt.xticks(rotation=45, ha='right')

    # Guardar el gráfico de barras por comuna en BytesIO
    with BytesIO() as image_stream_comuna_bar:
        plt.savefig(image_stream_comuna_bar, format='png', bbox_inches='tight')
        image_stream_comuna_bar.seek(0)
        image_base64_comuna_bar = base64.b64encode(image_stream_comuna_bar.getvalue()).decode('utf-8')

    # Convertir los datos a un DataFrame de pandas
    data_dict = {'Comunas': comunas, 'Cantidad de actividades por Comuna': cantidades_actividades_comuna}
    df = pd.DataFrame(data_dict)

    # Guardar el DataFrame como un archivo Excel
    excel_file_path = 'datosComunasActividades.xlsx'
    df.to_excel(excel_file_path, index=False)

    # -----------------------------------------------------------------------------------------------------------------------------------------

    # Crear el gráfico de torta por comuna
    fig_pie_comuna, ax_pie_comuna = plt.subplots(figsize=(8, 8))
    ax_pie_comuna.pie(cantidades_actividades_comuna, labels=comunas, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax_pie_comuna.set_title('Gráfico de Tortas (Comuna)')

    # Guardar el gráfico de torta por comuna en BytesIO
    with BytesIO() as image_stream_comuna_pie:
        plt.savefig(image_stream_comuna_pie, format='png', bbox_inches='tight')
        image_stream_comuna_pie.seek(0)
        image_base64_comuna_pie = base64.b64encode(image_stream_comuna_pie.getvalue()).decode('utf-8')

    # Obtener datos para el gráfico de barras por región
    actividades_por_region = Actividad.objects.values('region').annotate(total=Count('id'))

    # Crear el gráfico de barras por región
    regiones = [actividad['region'] for actividad in actividades_por_region]
    cantidades_actividades_region = [actividad['total'] for actividad in actividades_por_region]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(regiones, cantidades_actividades_region, color='lightcoral')
    ax.set_xlabel('Región')
    ax.set_ylabel('Cantidad de Actividades')
    ax.set_title('Gráfico de Barras (Región)')
    plt.xticks(rotation=45, ha='right')

    # Guardar el gráfico de barras por región en BytesIO
    with BytesIO() as image_stream_region_bar:
        plt.savefig(image_stream_region_bar, format='png', bbox_inches='tight')
        image_stream_region_bar.seek(0)
        image_base64_region_bar = base64.b64encode(image_stream_region_bar.getvalue()).decode('utf-8')

    # Crear el gráfico de torta por región
    fig_pie_region, ax_pie_region = plt.subplots(figsize=(8, 8))
    ax_pie_region.pie(cantidades_actividades_region, labels=regiones, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax_pie_region.set_title('Gráfico de Tortas (Región)')

    # Guardar el gráfico de torta por región en BytesIO
    with BytesIO() as image_stream_region_pie:
        plt.savefig(image_stream_region_pie, format='png', bbox_inches='tight')
        image_stream_region_pie.seek(0)
        image_base64_region_pie = base64.b64encode(image_stream_region_pie.getvalue()).decode('utf-8')

    # Convertir los datos a un DataFrame de pandas
    data_dict2 = {'Regiones': regiones, 'Cantidad de actividades por Región': cantidades_actividades_region}
    df2 = pd.DataFrame(data_dict2)

    # Guardar el DataFrame como un archivo Excel
    excel_file_path2 = 'datosRegionActividades.xlsx'
    df2.to_excel(excel_file_path2, index=False)

    # --------------------------------------------------------------------------------------------------------------------------------------------------------

    # Obtener datos para el gráfico de inscripciones por estado
    estados_inscripciones = [inscripcion.estado for inscripcion in Inscripcion.objects.all()]
    estado_counts = Counter(estados_inscripciones)

    # Crear el gráfico de torta de inscripciones por estado
    fig_torta_inscripciones, ax_torta_inscripciones = plt.subplots(figsize=(8, 8))
    ax_torta_inscripciones.pie(estado_counts.values(), labels=estado_counts.keys(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

    # Añadir leyenda
    ax_torta_inscripciones.legend(estado_counts.keys(), title="Estados", loc="center left", bbox_to_anchor=(1, 0.5))

    # Guardar el gráfico de torta en BytesIO
    with BytesIO() as image_stream_torta_inscripciones:
        plt.savefig(image_stream_torta_inscripciones, format='png', bbox_inches='tight')
        image_stream_torta_inscripciones.seek(0)
        image_base64_pie_inscripciones = base64.b64encode(image_stream_torta_inscripciones.getvalue()).decode('utf-8')

    # Crear el gráfico de barras de inscripciones por estado
    fig_barras_inscripciones, ax_barras_inscripciones = plt.subplots(figsize=(10, 6))
    ax_barras_inscripciones.bar(estado_counts.keys(), estado_counts.values(), color=plt.cm.Paired.colors)
    ax_barras_inscripciones.set_xlabel('Estados')
    ax_barras_inscripciones.set_ylabel('Cantidad de Inscripciones')

    # Ajustar el eje y para mostrar valores enteros
    ax_barras_inscripciones.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    ax_barras_inscripciones.set_ylim(0, 10)  # Cambiando el rango de valores del eje Y

    # Guardar el gráfico de barras en BytesIO
    with BytesIO() as image_stream_barras_inscripciones:
        plt.savefig(image_stream_barras_inscripciones, format='png', bbox_inches='tight')
        image_stream_barras_inscripciones.seek(0)
        image_base64_barras_inscripciones = base64.b64encode(image_stream_barras_inscripciones.getvalue()).decode('utf-8')

    # Convertir los datos a un DataFrame de pandas
    data_dict3 = {
        'Estados de Inscripciones': list(estado_counts.keys()), 
        }
    df3 = pd.DataFrame(data_dict3)

    # Calcular el porcentaje y agregarlo como una nueva columna en el DataFrame
    total_inscripciones = sum(estado_counts.values())
    df3['Porcentaje'] = [(count / total_inscripciones) * 100 for count in estado_counts.values()]

    # Formatear la columna de porcentaje con el símbolo "%"
    df3['Porcentaje'] = df3['Porcentaje'].apply(lambda x: f"{x:.2f}%")

    # Guardar el DataFrame como un archivo Excel
    excel_file_path3 = 'datosEstadoActividades.xlsx'
    df3.to_excel(excel_file_path3, index=False)

    # --------------------------------------------------------------------------------------------------------------------------------------------------------

    # Renderizar la plantilla con todos los conjuntos de gráficos
    return render(
        request,
        'dashboard/dashboard_actividad.html',
        {
            'image_base64_comuna_bar': image_base64_comuna_bar,
            'image_base64_comuna_pie': image_base64_comuna_pie,
            'image_base64_region_bar': image_base64_region_bar,
            'image_base64_region_pie': image_base64_region_pie,
            'image_base64_pie_inscripciones': image_base64_pie_inscripciones,
            'image_base64_barras_inscripciones': image_base64_barras_inscripciones,
            'excel_file_path': excel_file_path, 
            'excel_file_path2': excel_file_path2, 
            'excel_file_path3': excel_file_path3, 
        }
    )



@user_passes_test(lambda u: u.is_staff)
def dashboard_proyecto(request):
    # Obtener datos para el gráfico de solicitudes por estado
    estados_solicitudes = [solicitud.estado for solicitud in Solicitud.objects.all()]
    estado_counts = Counter(estados_solicitudes)

    # Lista de colores fijos
    colores = ['#FF9999', '#66B2FF', '#99FF99']

    # Crear el gráfico de torta de solicitudes por estado
    fig_torta_solicitudes, ax_torta_solicitudes = plt.subplots(figsize=(8, 8))
    ax_torta_solicitudes.pie(estado_counts.values(), labels=estado_counts.keys(), autopct='%1.1f%%', startangle=90, colors=colores)

    # Añadir leyenda
    ax_torta_solicitudes.legend(estado_counts.keys(), title="Estados", loc="center left", bbox_to_anchor=(1, 0.5))

    # Guardar el gráfico de torta en BytesIO
    with BytesIO() as image_stream_torta_solicitudes:
        plt.savefig(image_stream_torta_solicitudes, format='png', bbox_inches='tight')
        image_stream_torta_solicitudes.seek(0)
        image_base64_pie_solicitudes = base64.b64encode(image_stream_torta_solicitudes.getvalue()).decode('utf-8')
    
    # Convertir los datos a un DataFrame de pandas
    data_dict= {
        'Estados de las Solicitudes': list(estado_counts.keys()), 
    }
    df= pd.DataFrame(data_dict)

    # Calcular el porcentaje y agregarlo como una nueva columna en el DataFrame
    total_solicitudes = sum(estado_counts.values())
    df['Porcentaje'] = [(count / total_solicitudes) * 100 for count in estado_counts.values()]

    # Formatear la columna de porcentaje con el símbolo "%"
    df['Porcentaje'] = df['Porcentaje'].apply(lambda x: f"{x:.2f}%")

    # Guardar el DataFrame como un archivo Excel
    excel_file_path= 'datosEstadoProyectos.xlsx'
    df.to_excel(excel_file_path, index=False)

    # --------------------------------------------------------------------------------------------------------------------------------------

    # Crear el gráfico de barras de solicitudes por estado
    fig_barras_solicitudes, ax_barras_solicitudes = plt.subplots(figsize=(10, 6))
    ax_barras_solicitudes.bar(estado_counts.keys(), estado_counts.values(), color=colores)
    ax_barras_solicitudes.set_xlabel('Estados')
    ax_barras_solicitudes.set_ylabel('Cantidad de Solicitudes')

    # Ajustar el eje y para mostrar valores enteros
    ax_barras_solicitudes.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    ax_barras_solicitudes.set_ylim(0, 10)
    
    # Guardar el gráfico de barras en BytesIO
    with BytesIO() as image_stream_barras_solicitudes:
        plt.savefig(image_stream_barras_solicitudes, format='png', bbox_inches='tight')
        image_stream_barras_solicitudes.seek(0)
        image_base64_barras_solicitudes = base64.b64encode(image_stream_barras_solicitudes.getvalue()).decode('utf-8')

    # Convertir los datos a un DataFrame de pandas
    data_dict2 = {
        'Estados de Solicitudes': list(estado_counts.keys()), 
        'Cantidad de Solicitudes': list(estado_counts.values()),
        }
    df2 = pd.DataFrame(data_dict2)

    # Guardar el DataFrame como un archivo Excel
    excel_file_path2 = 'datosCantidadProyectos.xlsx'
    df2.to_excel(excel_file_path2, index=False)

    # Renderizar la plantilla con ambos gráficos
    return render(
        request,
        'dashboard/dashboard_proyecto.html',
        {
            'image_base64_pie_solicitudes': image_base64_pie_solicitudes,
            'image_base64_barras_solicitudes': image_base64_barras_solicitudes,
            'excel_file_path': excel_file_path,
            'excel_file_path2': excel_file_path2,
        }
    )



# Función adicional para manejar la descarga de los datos en el archivo Excel
def download_excel(request, file_path):
    with open(file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=datos.xlsx'
        return response
    
def download_excel_birthdate(request, file_path):
    with open(file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=datosNacimientoUsuarios.xlsx'
        return response
    

# ------------------------------------------------------------------------------------------

def download_excel_actividades_comuna(request, file_path):
    with open(file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=datosComunasActividades.xlsx'
        return response
    

def download_excel_actividades_region(request, file_path):
    with open(file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=datosRegionActividades.xlsx'
        return response
    

def download_excel_actividades_estado(request, file_path):
    with open(file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=datosEstadoActividades.xlsx'
        return response
    

# -----------------------------------------------------------------------------------------------

def download_excel_solicitudes_estado(request, file_path):
    with open(file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=datosEstadoProyectos.xlsx'
        return response
    

def download_excel_solicitudes_cantidad(request, file_path):
    with open(file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=datosCantidadProyectos.xlsx'
        return response
    
