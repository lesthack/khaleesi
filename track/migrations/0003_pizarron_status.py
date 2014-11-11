# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0002_auto_20141110_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizarron',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Asignado'), (1, b'Pendiente'), (2, b'En Proceso'), (3, b'Pausado'), (4, b'Terminado'), (5, b'Bloqueado'), (6, b'Reasignado')]),
            preserve_default=True,
        ),
    ]
