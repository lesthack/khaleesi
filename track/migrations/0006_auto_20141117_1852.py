# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0005_auto_20141117_0644'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='body',
            field=models.TextField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mail',
            name='context',
            field=models.TextField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
