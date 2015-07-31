# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0012_proyecto_repository'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulo',
            name='color',
            field=models.CharField(max_length=6, null=True, blank=True),
            preserve_default=True,
        ),
    ]
