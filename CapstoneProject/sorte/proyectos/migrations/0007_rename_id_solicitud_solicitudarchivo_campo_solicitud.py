# Generated by Django 4.2.6 on 2023-12-04 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0006_alter_solicitud_archivos_adjuntos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitudarchivo',
            old_name='id_solicitud',
            new_name='campo_solicitud',
        ),
    ]