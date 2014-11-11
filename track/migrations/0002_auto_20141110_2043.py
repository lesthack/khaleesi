# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('track', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='pizarron',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log', models.CharField(default=None, max_length=75, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tarea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=75)),
                ('descripcion', models.TextField()),
                ('fecha_inicial', models.DateTimeField(null=True)),
                ('fecha_final', models.DateTimeField(null=True)),
                ('horas_estimadas', models.IntegerField(default=None, null=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'Abierto'), (1, b'Cerrado')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modulo', models.ForeignKey(to='track.modulo')),
                ('responsable', models.ForeignKey(related_name='tarea_responsable', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pizarron',
            name='tarea',
            field=models.ForeignKey(to='track.tarea'),
            preserve_default=True,
        ),
    ]
