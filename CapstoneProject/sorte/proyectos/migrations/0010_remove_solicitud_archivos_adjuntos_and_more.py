# Generated by Django 4.2.6 on 2023-12-04 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0009_alter_solicitudarchivo_archivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud',
            name='archivos_adjuntos',
        ),
        migrations.AddField(
            model_name='solicitud',
            name='archivos_adjuntos',
            field=models.FileField(blank=True, upload_to='', verbose_name='SolicitudArchivo'),
        ),
    ]
