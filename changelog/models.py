# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

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
        return self.objeto.relacion_objeto
    get_objeto_cambio.short_description = 'Cambio'

    def nota_corta(self):
        nota = self.nota[0:120]
        if len(self.nota[120:]) > 0:
            nota = nota + '...'
        return nota
    nota_corta.short_description = 'Nota'
