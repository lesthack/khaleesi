# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.urlresolvers import reverse

class tipo_dato(models.Model):
    dato = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.dato

class tipo_objeto(models.Model):
    tipo = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.tipo

class objeto(models.Model):
    objeto = models.CharField(max_length=100)
    tipo = models.ForeignKey(tipo_objeto)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)
    relacion_objeto = models.ForeignKey('self', blank=True, null=True, related_name="relacion")
    tipo_dato = models.ForeignKey(tipo_dato, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, blank=True, null=True, default=None, related_name='objeto_deleted_by')
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __unicode__(self):
        return self.objeto
    
    def created_by_link(self):
        return format_html('<a href="#?created_by__id__exact={0}">{1}</a>', self.created_by.id, self.created_by.username)
    created_by_link.short_description = 'Created by'
    created_by_link.admin_order_field = 'created_by'

    def relacion_objeto_link(self):
        if self.relacion_objeto:
            return format_html('<a href="?relacion_objeto__id__exact={0}">{1}</a>', self.relacion_objeto.id, self.relacion_objeto.objeto)
        return '--'
    relacion_objeto_link.short_description = 'Relacion Objeto'    
    relacion_objeto_link.admin_order_field = 'relacion_objeto__objeto'

    def tipo_objeto_link(self):
        return format_html('<a href="?tipo__id__exact={0}">{1}</a>', self.tipo.id, self.tipo)
    tipo_objeto_link.short_description = 'Tipo objeto'
    tipo_objeto_link.admin_order_field = 'tipo'
    
    def tipo_dato_link(self):
        if self.tipo_dato:
            return format_html('<a href="?tipo__id__exact={0}">{1}</a>', self.tipo_dato.id, self.tipo_dato)
        return '--'
    tipo_dato_link.short_description = 'Tipo dato'
    tipo_dato_link.admin_order_field = 'tipo_dato'

class tipo_cambio(models.Model):
    tipo = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)
    descripcion = models.TextField()

    def __unicode__(self):
        return self.tipo

class cambio(models.Model):
    objeto = models.ForeignKey(objeto)
    tipo = models.ForeignKey(tipo_cambio)
    nota = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,blank=True,null=True)

    def __unicode__(self):
        return '{0}: {1}'.format(self.tipo, self.objeto)

    def get_objeto_cambio(self):
        return format_html('<a href="?q={0}">{0}</a>', self.objeto.relacion_objeto)
    get_objeto_cambio.short_description = 'Cambio'
    get_objeto_cambio.admin_order_field = 'objeto__relacion_objeto'
    
    def objeto_link(self):
        return format_html('<a href="?objeto__id__exact={0}">{1}</a>', self.objeto.id, self.objeto)
    objeto_link.short_description = 'Objeto'
    objeto_link.admin_order_field = 'objeto'

    def tipo_link(self):
        return format_html('<a href="?tipo__id__exact={0}">{1}</a>', self.tipo.id, self.tipo)
    tipo_link.short_description = 'Tipo'
    tipo_link.admin_order_field = 'tipo'

    def nota_corta(self):
        nota = self.nota[0:120]
        if len(self.nota[120:]) > 0:
            nota = nota + '...'
        return nota
    nota_corta.short_description = 'Nota'
    nota_corta.admin_order_field = 'nota'

    def created_by_link(self):
        return format_html('<a href="#?created_by__id__exact={0}">{1}</a>', self.created_by.id, self.created_by.username)
    created_by_link.short_description = 'Created by'
    created_by_link.admin_order_field = 'created_by'
