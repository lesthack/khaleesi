# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('track', '0004_auto_20141110_2315'),
    ]

    operations = [
        migrations.CreateModel(
            name='mail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=100)),
                ('context', models.TextField()),
                ('template', models.CharField(max_length=100)),
                ('sended', models.BooleanField(default=False)),
                ('error', models.BooleanField(default=False)),
                ('error_description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='email_created_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('send_to', models.ForeignKey(related_name='email_send_to', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='pizarron',
            name='log',
            field=models.CharField(default=None, max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pizarron',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Asignado'), (1, b'Pendiente'), (2, b'En Proceso'), (3, b'Pausado'), (4, b'Terminado'), (5, b'Bloqueado'), (6, b'Reasignado'), (7, b'Abandonada')]),
            preserve_default=True,
        ),
    ]
