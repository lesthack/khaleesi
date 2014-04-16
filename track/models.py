# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html

class proyecto(models.Model):
    proyecto = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=1024, blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, blank=True, null=True, default=None, related_name='proyecto_deleted_by')
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __unicode__(self):
        return self.proyecto

    def activos(self):
        return format_html('<a href="/admin/track/modulo/?q=&proyecto__proyecto={0}&deleted__exact=0">{1}</a>', self.proyecto, modulo.objects.filter(proyecto=self, deleted=False).count())

    def cancelados(self):
        return format_html('<a href="/admin/track/modulo/?q=&proyecto__proyecto={0}&deleted__exact=1">{1}</a>', self.proyecto, modulo.objects.filter(proyecto=self, deleted=True).count())

class modulo(models.Model):
    proyecto = models.ForeignKey(proyecto)
    modulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, blank=True, null=True, default=None, related_name='modulo_deleted_by')
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __unicode__(self):
        return self.modulo

    def proyecto_link(self):
        return format_html('<a href="/admin/track/proyecto/{0}/">{1}</a>', self.proyecto.id, self.proyecto)
    proyecto_link.short_description = 'Proyecto'
    proyecto_link.allow_tags = True
    proyecto_link.admin_order_field = 'proyecto'

    def issues_resueltos(self):
        return format_html('<a href="/admin/track/issue/?q=&modulo__modulo={0}&status__exact=1">{1}</a>', self.modulo, issue.objects.filter(modulo=self, status=1).count())
    issues_resueltos.short_description = 'Resueltos'
    
    def issues_abiertos(self):
        return format_html('<a href="/admin/track/issue/?q=&status__exact=0">{0}</a>', issue.objects.filter(modulo=self, status=0).count())
    issues_abiertos.short_description = 'Abiertos'

    def issues_abandonados(self):
        return format_html('<a href="/admin/track/issue/?q=&status__exact=2">{0}</a>', issue.objects.filter(modulo=self, status=2).count())
    issues_abandonados.short_description = 'Abandonados'

    def issues_cancelados(self):
        return format_html('<a href="/admin/track/issue/?q=&status__exact=3">{0}</a>', issue.objects.filter(modulo=self, status=3).count())
    issues_cancelados.short_description = 'Cancelados'

class tipo_issue(models.Model):
    tipo = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)
    
    def __unicode__(self):
        return self.tipo

class issue(models.Model):
    URGENCIA_CHOICES = (
        (0, 'Baja'),
        (1, 'Normal'),
        (2, 'Alta')
    )
    IMPORTANCIA_CHOICES = (
        (0, 'Normal'),
        (1, 'Importante'),
        (2, 'Esencial')
    )
    STATUS_CHOICES = (
        (0, 'Abierto'),
        (1, 'Resuelto'),
        (2, 'Abandonado'),
        (3, 'Cancelado')
    )
    modulo = models.ForeignKey(modulo)
    tipo_issue = models.ForeignKey(tipo_issue, default=1)
    urgencia = models.IntegerField(choices=URGENCIA_CHOICES, default=1)
    importancia = models.IntegerField(choices=IMPORTANCIA_CHOICES, default=0)
    descripcion = models.TextField()
    asignado_a = models.ForeignKey(User, related_name='asignado_a')
    link = models.CharField(max_length=1024, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)
    updated_by = models.ForeignKey(User, blank=True, null=True, related_name='updated_by')

    def __unicode__(self):
        return '{0}'.format(self.id)

    def proyecto_link(self):
        return format_html('<a href="/admin/track/proyecto/{0}/">{1}</a>', self.modulo.proyecto.id, self.modulo.proyecto)
    proyecto_link.short_description = 'Proyecto'
    proyecto_link.allow_tags = True
    proyecto_link.admin_order_field = 'modulo__proyecto'

    def modulo_link(self):
        return format_html('<a href="/admin/track/modulo/{0}/">{1}</a>', self.modulo.id, self.modulo)
    modulo_link.short_description = 'Modulo'
    modulo_link.allow_tags = True
    modulo_link.admin_order_field = 'modulo'

    def is_closed(self):
        if self.status == 0:
            return False
        return True

    def get_notas(self):
        return issue_nota.objects.filter(issue=self).order_by('-created_at', 'like')

class issue_nota(models.Model):
    issue = models.ForeignKey(issue)
    nota = models.TextField()
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return '{0}'.format(self.id)
