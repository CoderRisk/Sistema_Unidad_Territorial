# Generated by Django 4.2.6 on 2023-12-04 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0010_remove_solicitud_archivos_adjuntos_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud',
            name='archivos_adjuntos',
        ),
        migrations.AddField(
            model_name='solicitud',
            name='archivos_adjuntos',
            field=models.ManyToManyField(blank=True, to='proyectos.solicitudarchivo'),
        ),
    ]
