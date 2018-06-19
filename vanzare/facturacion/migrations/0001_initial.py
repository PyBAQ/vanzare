# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-06 21:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=200)),
                ('tipo_identificacion', models.CharField(choices=[('cedula', 'C\xe9dula'), ('nit', 'NIT')], default='cedula', max_length=15)),
                ('numero_identificacion', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
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
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('detalle', models.CharField(blank=True, default='', max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('ancho', models.PositiveIntegerField(blank=True, help_text='Los valores deben estar en cent\xedmetros', null=True)),
                ('alto', models.PositiveIntegerField(blank=True, help_text='Los valores deben estar en cent\xedmetros', null=True)),
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
                ('valor', models.PositiveIntegerField(blank=True, help_text='Este ser\xe1 el valor unitario o el valor por docena, dependiendo del caso', null=True)),
                ('valor_cantidad', models.PositiveIntegerField(blank=True, null=True)),
                ('factor', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('especificacion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Especificaci\xf3n')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
                ('opciones_cobro', models.CharField(choices=[('estandar', 'Precio est\xe1ndar'), ('personalizado', 'Personalizado'), ('fijo', 'Fijo'), ('por_docena', 'Por docena')], max_length=100)),
            ],
            options={
                'verbose_name': 'Producto Base',
                'verbose_name_plural': 'Productos Base',
            },
        ),
        migrations.CreateModel(
            name='Recaudo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.PositiveIntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Recaudo',
                'verbose_name_plural': 'Recaudos',
            },
        ),
        migrations.CreateModel(
            name='Recibido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descuento', models.IntegerField(default=0)),
                ('abono', models.IntegerField(default=0)),
                ('saldo', models.IntegerField(default=0)),
                ('subtotal', models.PositiveIntegerField(default=0)),
                ('total', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True, null=True)),
                ('recaudado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacion.Cliente')),
            ],
            options={
                'verbose_name': 'Recibido',
                'verbose_name_plural': 'Recibidos',
            },
        ),
        migrations.AddField(
            model_name='recaudo',
            name='recibido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacion.Recibido'),
        ),
        migrations.AddField(
            model_name='producto',
            name='producto_base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacion.ProductoBase'),
        ),
        migrations.AddField(
            model_name='producto',
            name='recibido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacion.Recibido'),
        ),
    ]