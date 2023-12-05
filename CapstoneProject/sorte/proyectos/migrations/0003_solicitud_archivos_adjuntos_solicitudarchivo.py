# Generated by Django 4.2.6 on 2023-12-04 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0002_remove_solicitud_archivos_adjuntos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='archivos_adjuntos',
            field=models.FileField(blank=True, null=True, upload_to='solicitudes_archivos/'),
        ),
        migrations.CreateModel(
            name='SolicitudArchivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='solicitudes_archivos/')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos.solicitud')),
            ],
        ),
    ]