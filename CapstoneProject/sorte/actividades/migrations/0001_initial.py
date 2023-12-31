# Generated by Django 4.2.6 on 2023-10-23 22:14

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
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen_actividad', models.ImageField(blank=True, null=True, upload_to='actividades')),
                ('nombre_actividad', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('direccion', models.CharField(max_length=200)),
                ('region', models.CharField(choices=[('RM', 'Región Metropolitana')], default='RM', max_length=100)),
                ('comuna', models.CharField(choices=[('Isla de Maipo', 'Isla de Maipo')], default='Isla de Maipo', max_length=100)),
                ('fecha_actividad', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_termino', models.TimeField()),
                ('cupos_disponibles', models.IntegerField(default=20)),
            ],
            options={
                'verbose_name': 'actividad',
                'verbose_name_plural': 'actividades',
            },
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], default='pendiente', max_length=20)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.actividad')),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
