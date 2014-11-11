# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('urgencia', models.IntegerField(default=1, choices=[(0, b'Baja'), (1, b'Normal'), (2, b'Alta')])),
                ('importancia', models.IntegerField(default=0, choices=[(0, b'Normal'), (1, b'Importante'), (2, b'Esencial')])),
                ('descripcion', models.TextField()),
                ('link', models.CharField(max_length=1024, null=True, blank=True)),
                ('status', models.IntegerField(default=0, choices=[(0, b'Abierto'), (1, b'Resuelto'), (2, b'Abandonado'), (3, b'Cancelado')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asignado_a', models.ForeignKey(related_name='issue_asignado_a', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='issue_nota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nota', models.TextField()),
                ('like', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('issue', models.ForeignKey(to='track.issue')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='modulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(default=None, null=True, blank=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('deleted_by', models.ForeignKey(related_name='modulo_deleted_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='proyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proyecto', models.CharField(max_length=100)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('link', models.CharField(max_length=1024, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(default=None, null=True, blank=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('deleted_by', models.ForeignKey(related_name='proyecto_deleted_by', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tipo_issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='modulo',
            name='proyecto',
            field=models.ForeignKey(to='track.proyecto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='modulo',
            field=models.ForeignKey(to='track.modulo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='tipo_issue',
            field=models.ForeignKey(default=1, to='track.tipo_issue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
