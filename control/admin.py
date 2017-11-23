# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from .models import *
from khaleesi.hacks import *
from hashlib import md5
import datetime

class tokenForm(forms.ModelForm):
    class Meta:
        model = token
        exclude = ['created_by', 'created_at']
    
    def __init__(self, *args, **kwargs):
        if not kwargs.get('instance', False):
            if not kwargs.get('initial'):
                kwargs['initial'] = {}
            kwargs['initial'].update({'token': md5(str(datetime.datetime.now())).hexdigest()})
        super(tokenForm, self).__init__(*args, **kwargs)
        self.fields['token'].widget.attrs['readonly'] = True

@admin.register(token)
class tokenAdmin(nModelAdmin):
    list_display = ['user', 'token', 'begins_at', 'expire_at']
    list_display_links = ['token']
    list_display_mobile = ['user', 'token']
    search_fields = ['user__username']
    list_filter = ['begins_at', 'expire_at']
    form = tokenForm

@admin.register(sqlview)
class sqlviewAdmin(nModelAdmin):
    list_display = ['sql_name', 'title', 'enable']
    list_display_links = ['sql_name', 'title']
    list_display_mobile = ['sql_name', 'enable']
    search_fields = ['sql_name', 'title']
    list_filter = ['enable', 'group']
