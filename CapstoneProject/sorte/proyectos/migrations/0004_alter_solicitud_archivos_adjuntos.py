# Generated by Django 4.2.6 on 2023-12-04 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0003_solicitud_archivos_adjuntos_solicitudarchivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='archivos_adjuntos',
            field=models.FileField(blank=True, null=True, upload_to='archivos_solicitudes/'),
        ),
    ]
