# Generated by Django 3.2 on 2021-05-06 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misPerris', '0002_mascota'),
    ]

    operations = [
        migrations.AddField(
            model_name='mascota',
            name='imagen',
            field=models.ImageField(null=True, upload_to='mascotas'),
        ),
    ]