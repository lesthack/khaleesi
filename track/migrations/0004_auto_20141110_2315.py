# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0003_pizarron_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='horas_estimadas',
            field=models.IntegerField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
