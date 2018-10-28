# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-10-28 00:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('detalle', models.CharField(blank=True, default='', max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('ancho', models.PositiveIntegerField(blank=True, help_text='Los valores deben estar en centímetros', null=True)),
                ('alto', models.PositiveIntegerField(blank=True, help_text='Los valores deben estar en centímetros', null=True)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='ProductoBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('valor', models.PositiveIntegerField(blank=True, help_text='Este será el valor unitario o el valor por docena, dependiendo del caso', null=True)),
                ('valor_cantidad', models.PositiveIntegerField(blank=True, null=True)),
                ('factor', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('especificacion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Especificación')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
                ('opciones_cobro', models.CharField(choices=[('estandar', 'Precio estándar'), ('personalizado', 'Personalizado'), ('por_docena', 'Por docena')], max_length=100)),
            ],
            options={
                'verbose_name': 'Producto Base',
                'verbose_name_plural': 'Productos Base',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='producto_base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.ProductoBase'),
        ),
        migrations.AddField(
            model_name='producto',
            name='recibido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.Recibido'),
        ),
    ]
