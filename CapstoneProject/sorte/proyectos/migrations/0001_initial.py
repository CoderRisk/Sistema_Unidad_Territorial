# Generated by Django 4.2.6 on 2023-11-22 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen_proyecto', models.ImageField(blank=True, null=True, upload_to='proyectos')),
                ('nombre_proyecto', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('requisitos', models.TextField()),
                ('cupos_disponibles_proyecto', models.IntegerField(default=0)),
                ('fecha_creacion_proyecto', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion_proyecto', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización del proyecto')),
            ],
            options={
                'verbose_name': 'proyecto',
                'verbose_name_plural': 'proyectos',
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], default='pendiente', max_length=10)),
                ('fecha_solicitud', models.DateTimeField(auto_now_add=True)),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos.proyecto')),
            ],
        ),
    ]
