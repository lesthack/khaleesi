# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0010_auto_20160317_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='show_resume',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
