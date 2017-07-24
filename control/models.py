# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from khaleesi.sensible import *
from datetime import datetime
import ast
import random

class token(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=254, unique=True)
    begins_at = models.DateTimeField()
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,blank=True, null=True,related_name='token_created_by')

    def __unicode__(self):
        return u'{}'.format(self.token)

class sqlview(models.Model):
    sql_name = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    enable = models.BooleanField(default=False)
    group = models.ForeignKey(Group, blank=True, null=True)

    def __unicode__(self):
        return u'{}: {}'.format(self.title, self.sql_name)

class uses_view(models.Model):
    user = models.ForeignKey(User)
    sqlview = models.ForeignKey(sqlview)
    created_at = models.DateTimeField(auto_now_add=True)

