# Generated by Django 4.2.6 on 2023-12-04 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0006_solicitudinscripcion_inscripcion_archivos_adjuntos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripcion',
            name='archivos_adjuntos',
            field=models.ManyToManyField(blank=True, related_name='archivos_adjuntos', to='actividades.solicitudinscripcion'),
        ),
    ]
