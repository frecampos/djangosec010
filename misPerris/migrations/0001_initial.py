# Generated by Django 3.2 on 2021-05-05 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('nombre', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('anno', models.IntegerField()),
            ],
        ),
    ]
