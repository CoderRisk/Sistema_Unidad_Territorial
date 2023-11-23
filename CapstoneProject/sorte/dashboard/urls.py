from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicioDashboard, name="inicioDashboard"),
    # Path para visualizar el gráfico de género
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard_actividad/', views.dashboard_actividad, name='dashboard_actividad'),
    path('dashboard_proyecto/', views.dashboard_proyecto, name='dashboard_proyecto'),
    path('download_excel/<str:file_path>/', views.download_excel, name='download_excel'),
    path('download_excel_birthdate/<str:file_path>/', views.download_excel_birthdate, name='download_excel_birthdate'),
    path('download_excel_actividades_comuna/<str:file_path>/', views.download_excel_actividades_comuna, name='download_excel_actividades_comuna'),
    path('download_excel_actividades_region/<str:file_path>/', views.download_excel_actividades_region, name='download_excel_actividades_region'),
    path('download_excel_actividades_estado/<str:file_path>/', views.download_excel_actividades_estado, name='download_excel_actividades_estado'),
    path('download_excel_solicitudes_estado/<str:file_path>/', views.download_excel_solicitudes_estado, name='download_excel_solicitudes_estado'),
    path('download_excel_solicitudes_cantidad/<str:file_path>/', views.download_excel_solicitudes_cantidad, name='download_excel_solicitudes_cantidad'),
]