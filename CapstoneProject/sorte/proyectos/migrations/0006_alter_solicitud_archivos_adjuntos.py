# Generated by Django 4.2.6 on 2023-12-04 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0005_rename_solicitud_solicitudarchivo_id_solicitud_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='archivos_adjuntos',
            field=models.ManyToManyField(blank=True, to='proyectos.solicitudarchivo'),
        ),
    ]
