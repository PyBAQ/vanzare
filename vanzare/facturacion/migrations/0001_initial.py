# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-28 00:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElementoGasto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Elemento de Gasto',
                'verbose_name_plural': 'Elementos de Gasto',
            },
        ),
        migrations.CreateModel(
            name='Gasto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.PositiveIntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
                ('elemento_gasto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacion.ElementoGasto')),
            ],
            options={
                'verbose_name': 'Gasto',
                'verbose_name_plural': 'Gastos',
            },
        ),
    ]
