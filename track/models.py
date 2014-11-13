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
        return format_html(u'<a href="/admin/track/modulo/?q=&proyecto__proyecto={0}&deleted__exact=0">{1}</a>', self.proyecto, modulo.objects.filter(proyecto=self, deleted=False).count())

    def cancelados(self):
        return format_html(u'<a href="/admin/track/modulo/?q=&proyecto__proyecto={0}&deleted__exact=1">{1}</a>', self.proyecto, modulo.objects.filter(proyecto=self, deleted=True).count())

    def gantt_link(self):
        return format_html(u'<a href="/admin/track/proyecto/{}/gantt/">Ver</a>'.format(self.id))
    gantt_link.short_description = 'Gantt'
    gantt_link.allow_tags = True

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
        return '{0}->{1}'.format(self.proyecto, self.modulo)

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

class tarea(models.Model):
    STATUS_CHOICES = (
        (0, 'Abierto'),
        (1, 'Cerrado')
    )
    modulo = models.ForeignKey(modulo)
    nombre = models.CharField(max_length=75)
    descripcion = models.TextField()
    fecha_inicial = models.DateTimeField(null=True)
    fecha_final = models.DateTimeField(null=True)
    horas_estimadas = models.IntegerField(blank=True, null=True, default=None)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    responsable = models.ForeignKey(User, related_name='tarea_responsable')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)
    
    def __unicode__(self):
        return '{}'.format(self.id)

    def get_horas_estimadas(self):
        if self.horas_estimadas:
            return self.horas_estimadas
        return 0
    get_horas_estimadas.short_description = 'Hrs Estimadas'

    def get_horas_reales(self):
        horas = 0
        dateini = None
        datefin = None
        last_status = None
        list_pizarron = pizarron.objects.filter(tarea=self).order_by('created_at')
        
        for view_pizarron in list_pizarron:
            if view_pizarron.status == 2 and last_status != 2:                
                dateini = view_pizarron.created_at
            if view_pizarron.status != 2:
                datefin = view_pizarron.created_at
                if dateini and datefin:
                    horas_lambda = datefin - dateini
                    horas += horas_lambda.seconds/3600
                    #minutos = horas_lambda.seconds%3600/60
                    dateini = None

            last_status = view_pizarron.status

        return horas
    get_horas_reales.short_description = 'Hrs Reales'

    def get_last_log(self):
        try:
            return pizarron.objects.filter(tarea=self).order_by('-created_at')[:1][0]
        except:
            return None

    def get_color_status(self):
        colors = {
            0: '#8A2BE2', # purple - Asignado
            1: '#FFA500', # yellow - Pendiente
            2: '#00008B', # blue - En Proceso
            3: '#FF4500', # orange - Pausado
            4: '#006400', # green - Terminado
            5: '#8B0000', # red - Bloqueado
            6: '#8A2BE2', # purple - Reasignado
            7: '#778899', # grey - Abandonada
        }
        try:
            return colors[self.get_last_log().status]
        except:
            return colors[0]

    def get_last_status(self):
        try:
            return self.get_last_log().get_status()
        except:
            return 'Sin actividad'

    def get_pizarron(self):
        return format_html(u'<span style="color: {1};">{0}</span>'.format(self.get_last_status(), self.get_color_status()))
    get_pizarron.short_description = 'Pizarrón'

    def proyecto_link(self):
        return self.modulo.proyecto_link()
    proyecto_link.short_description = 'Proyecto'
    proyecto_link.allow_tags = True
    proyecto_link.admin_order_field = 'proyecto'

    def modulo_link(self):
        return format_html('<a href="/admin/track/modulo/{0}/">{1}</a>', self.modulo.id, self.modulo.modulo)
    modulo_link.short_description = 'Modulo'
    modulo_link.allow_tags = True
    modulo_link.admin_order_field = 'modulo'

    def responsable_link(self):
        return format_html('<a href="/admin/track/user/{0}/proyecto/{1}/gantt/">{2}</a>', self.responsable.id, self.modulo.proyecto.id, self.responsable.username)
    responsable_link.short_description = 'Responsable'
    responsable_link.allow_tags = True
    responsable_link.admin_order_field = 'responsable'

class pizarron(models.Model):
    STATUS_CHOICES = (
        (0, 'Asignado'),
        (1, 'Pendiente'),
        (2, 'En Proceso'),
        (3, 'Pausado'),
        (4, 'Terminado'),
        (5, 'Bloqueado'),
        (6, 'Reasignado'),
        (7, 'Abandonada'),
    )
    tarea = models.ForeignKey(tarea)
    log = models.CharField(max_length=75, null=True, default=None, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __unicode__(self):
        return '{}'.format(self.id)
    
    def save(self, *args, **kwargs):
        if self.status > 1:
            self.log = u'{0} ha marcado como {1} la tarea {2}.'.format(self.created_by.username, self.get_status(), self.tarea.id)
            if self.status == 4:
                self.tarea.status = 1
                self.tarea.save()
            elif self.status == 6:
                self.tarea.status = 0
                self.tarea.save()
        super(pizarron, self).save(*args, **kwargs)

    def get_status(self):
        return self.STATUS_CHOICES[self.status][1]

    def proyecto_link(self):
        return self.tarea.proyecto_link()
    proyecto_link.short_description = 'Proyecto'
    proyecto_link.allow_tags = True
    proyecto_link.admin_order_field = 'tarea__modulo__proyecto'

    def modulo_link(self):
        return self.tarea.modulo_link()
    modulo_link.short_description = 'Modulo'
    modulo_link.allow_tags = True
    modulo_link.admin_order_field = 'modulo'

    def tarea_link(self):
        return format_html(u'<a href="/admin/track/tarea/{0}/">{1}</a>', self.tarea.id, self.tarea.nombre)
    tarea_link.short_description = 'Tarea'
    tarea_link.allow_tags = True
    tarea_link.admin_order_field = 'tarea'

    def responsable_link(self):
        return format_html('<a href="/admin/track/user/{0}/proyecto/{1}/gantt/">{2}</a>', self.tarea.responsable.id, self.tarea.modulo.proyecto.id, self.tarea.responsable)
    responsable_link.short_description = 'Responsable'
    responsable_link.allow_tags = True
    responsable_link.admin_order_field = 'tarea__responsable'

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
    asignado_a = models.ForeignKey(User, related_name='issue_asignado_a')
    link = models.CharField(max_length=1024, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)
    updated_by = models.ForeignKey(User, blank=True, null=True, related_name='updated_by')

    def __unicode__(self):
        return '{0}'.format(self.id)

    def get_status(self):
        return self.STATUS_CHOICES[self.status][1]

    def get_urgencia(self):
        return self.URGENCIA_CHOICES[self.urgencia][1]

    def get_importancia(self):
        return self.IMPORTANCIA_CHOICES[self.importancia][1]

    def proyecto_link(self):
        return format_html('<a href="/admin/track/proyecto/{0}/">{1}</a>', self.modulo.proyecto.id, self.modulo.proyecto)
    proyecto_link.short_description = 'Proyecto'
    proyecto_link.allow_tags = True
    proyecto_link.admin_order_field = 'modulo__proyecto'

    def modulo_link(self):
        return format_html('<a href="/admin/track/modulo/{0}/">{1}</a>', self.modulo.id, self.modulo.modulo)
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
