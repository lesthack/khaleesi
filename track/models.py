# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from tastypie.models import *
from khaleesi.sensible import *
from datetime import datetime
import ast
import random
from github import Github

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_email_active = models.BooleanField(default=True)
    token = models.CharField(max_length=50, blank=True, null=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    lunch_time = models.TimeField(null=True, blank=True)
    sun = models.BooleanField(default=False)
    mon = models.BooleanField(default=True)
    tue = models.BooleanField(default=True)
    wed = models.BooleanField(default=True)
    thu = models.BooleanField(default=True)
    fri = models.BooleanField(default=True)
    sat = models.BooleanField(default=False)
    github = models.CharField(max_length=50, blank=True, null= True)

    def get_github_user(self):
        if len(self.github) > 0:
            usergit = Github(self.github)
            return usergit
        else:
            return None

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
    repository = models.CharField(max_length=1024, blank=True, null=True)

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

    def get_repo_info(self):
        if len(self.repository) > 0:
            repo_split = self.repository.split('/')
            return (repo_split[3], repo_split[4])

    def get_github_repo(self, gitUser):
        username, reponame = self.get_repo_info()
        return gitUser.get_user().get_repo(reponame)

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
    color = models.CharField(max_length=6, blank=True, null=True)

    def __unicode__(self):
        return u'{0}->{1}'.format(self.proyecto, self.modulo)

    def proyecto_link(self):
        return format_html('<a href="/admin/track/proyecto/{0}/">{1}</a>', self.proyecto.id, self.proyecto)
    proyecto_link.short_description = 'Proyecto'
    proyecto_link.allow_tags = True
    proyecto_link.admin_order_field = 'proyecto'

    def issues_resueltos(self):
        return format_html(u'<a href="/admin/track/issue/?q=&modulo__modulo={0}&status__exact=1">{1}</a>', self.modulo, issue.objects.filter(modulo=self, status=1).count())
    issues_resueltos.short_description = 'Resueltos'
    
    def issues_abiertos(self):
        return format_html(u'<a href="/admin/track/issue/?q=&status__exact=0">{0}</a>', issue.objects.filter(modulo=self, status=0).count())
    issues_abiertos.short_description = 'Abiertos'

    def issues_abandonados(self):
        return format_html(u'<a href="/admin/track/issue/?q=&status__exact=2">{0}</a>', issue.objects.filter(modulo=self, status=2).count())
    issues_abandonados.short_description = 'Abandonados'

    def issues_cancelados(self):
        return format_html(u'<a href="/admin/track/issue/?q=&status__exact=3">{0}</a>', issue.objects.filter(modulo=self, status=3).count())
    issues_cancelados.short_description = 'Cancelados'

    def create_github_label(self):
        if len(self.proyecto.repository) > 0:
            try:
                view_user_profile = UserProfile.objects.get(user=self.created_by)
                view_proyecto = self.proyecto
                usergit = view_user_profile.get_github_user()
                view_repo = view_proyecto.get_github_repo(usergit)
                view_repo.create_label(self.modulo, self.color)
            except Exception, e:
                pass

    def update_github_label(self):
        if len(self.proyecto.repository) > 0:
            try:
                view_user_profile = UserProfile.objects.get(user=self.created_by)
                view_proyecto = self.proyecto
                usergit = view_user_profile.get_github_user()
                view_repo = view_proyecto.get_github_repo(usergit)
                exist_label = False
                for label in view_repo.get_labels():
                    if label.name == self.modulo:
                        exist_label = True
                        label.edit(self.modulo, self.color)
                if not exist_label:
                    self.create_github_label()
            except Exception, e:
                pass

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

    def get_status(self):
        return self.STATUS_CHOICES[self.status][1]

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
                    horas += horas_lambda.total_seconds()
                    dateini = None
            last_status = view_pizarron.status

        return horas/3600
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

    def get_last_status_number(self):
        try:
            return self.get_last_log().get_status_number()
        except:
            return -1

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
            if self.status in [4, 7]:
                self.tarea.status = 1
                self.tarea.save()
            elif self.status == 6:
                self.tarea.status = 0
                self.tarea.save()
        super(pizarron, self).save(*args, **kwargs)

    def get_status(self):
        return self.STATUS_CHOICES[self.status][1]

    def get_status_number(self):
        return self.STATUS_CHOICES[self.status][0]

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

    def get_descripcion(self):
        sizestr = 80
        if len(self.descripcion) < sizestr:
            return strip_tags(self.descripcion)
        return strip_tags(self.descripcion[0:sizestr]) + '...'
    get_descripcion.short_description = 'Descripcion'
    get_descripcion.allow_tags = True
    get_descripcion.admin_order_field = 'descripcion'

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

    def github(self):
        if len(self.modulo.proyecto.repository) > 0:
            try:
                view_user_profile = UserProfile.objects.get(user=self.created_by)
                view_proyecto = self.modulo.proyecto
                usergit = view_user_profile.get_github_user()
                view_repo = view_proyecto.get_github_repo(usergit)
                view_repo_label = view_repo.get_label(self.modulo.modulo)
                view_repo.create_issue('Issue - Khaleesi #{}'.format(self.id), body = u'{}'.format(self.get_descripcion()), labels = [view_repo_label])
            except Exception, e:
                print 'Algo pasa'
                pass

class issue_nota(models.Model):
    issue = models.ForeignKey(issue)
    nota = models.TextField()
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return '{0}'.format(self.id)

class mail(models.Model):
    """list email to send"""
    subject = models.CharField(max_length=100)
    context = models.TextField(null=True, blank=True, default=None)
    body = models.TextField(null=True, blank=True, default=None)
    template = models.CharField(null=True, blank=True, default=None, max_length=100)
    send_to = models.ForeignKey(User,blank=True,null=True,related_name='email_send_to')
    sended = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    error_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,blank=True, null=True,related_name='email_created_by')
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
      return '{}'.format(self.id)

    def send(self):
        try:
            if self.context:
                template_html = get_template(str(self.template))
                html_content = template_html.render(Context(ast.literal_eval(self.context)))
            else:
                html_content = self.body
            msg_email = EmailMultiAlternatives(self.subject, html_content, EMAIL_DEFAULT, [self.send_to.email, ])
            msg_email.attach_alternative(html_content,'text/html')
            msg_email.send()
            self.sended = True
        except Exception, e:
            self.sended = False
            self.error = True
            self.error_description = 'the error %s' % (str(e))
        self.save()

class cita(models.Model):
    descripcion = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, blank=True, null=True, default=None, related_name='cita_deleted_by')
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    def __unicode__(self):
        return self.descripcion

# Extensiones al modelo User [Tal vez deberian separarse en otro archivo]
def user_get_tareas(self, status=[0,1]):
    """
        Tareas de un usuario.
        Filtro:
            status = [0] Abiertas
            status = [1] Cerradas
            status = [0,1] Todas
    """
    return tarea.objects.filter(responsable=self, status__in=status).order_by('fecha_inicial','fecha_final','horas_estimadas')

def user_get_tareas_abiertas_bloqueadas(self):
    piz = pizarron.objects.filter(status=5)
    return tarea.objects.filter(responsable=self, status=0, id__in=(p.tarea_id for p in piz)).order_by('fecha_inicial','fecha_final','horas_estimadas')

def user_get_tareas_abiertas(self):
    piz = pizarron.objects.filter(status=5)
    return tarea.objects.filter(responsable=self, status=0).exclude(id__in=(p.tarea_id for p in piz)).order_by('fecha_inicial','fecha_final','horas_estimadas')

def user_get_tareas_abiertas_cantidad(self):
    return self.get_tareas_abiertas() | self.get_tareas_abiertas_bloqueadas()

def user_get_tareas_cerradas(self):
    return self.get_tareas(status=[1])

def user_get_issues(self, status=[0,1,2,3]):
    return issue.objects.filter(asignado_a=self, status__in=status).order_by('status', '-urgencia', '-importancia', 'created_at')

def user_get_issues_abiertos(self):
    return self.get_issues(status=[0])

def user_get_10_issues_abiertos(self):
    return self.get_issues_abiertos()[0:10]

def user_get_tareas_activas(self):
    return tarea.objects.raw('SELECT id FROM track_tarea WHERE status=0 AND (SELECT status FROM track_pizarron WHERE tarea_id=track_tarea.id ORDER BY created_at DESC LIMIT 1 OFFSET 0)=2 AND responsable_id={user_id};'.format(user_id=self.id))

def user_get_tareas_recientes(self, n=3):
    return tarea.objects.raw('SELECT track_tarea.* \
            FROM track_tarea \
            WHERE \
                    responsable_id = {user_id} and status = 0 \
                AND (SELECT status FROM track_pizarron WHERE tarea_id=track_tarea.id ORDER BY created_at DESC LIMIT 1 OFFSET 0) IN (1,3) \
                AND (SELECT count(*) FROM track_pizarron WHERE tarea_id=track_tarea.id) > 1 \
            ORDER BY (SELECT updated_at FROM track_pizarron WHERE tarea_id=track_tarea.id ORDER BY created_at DESC LIMIT 1 OFFSET 0) DESC \
            LIMIT {n} OFFSET 0'.format(user_id=self.id, n=n))

def user_get_apikey(self):
    return '{}'.format(ApiKey.objects.get(user=self).key)

User.add_to_class('get_tareas', user_get_tareas)
User.add_to_class('get_tareas_abiertas', user_get_tareas_abiertas)
User.add_to_class('get_tareas_abiertas_bloqueadas', user_get_tareas_abiertas_bloqueadas)
User.add_to_class('get_tareas_abiertas_cantidad', user_get_tareas_abiertas_cantidad)
User.add_to_class('get_tareas_cerradas', user_get_tareas_cerradas)
User.add_to_class('get_issues', user_get_issues)
User.add_to_class('get_issues_abiertos', user_get_issues_abiertos)
User.add_to_class('get_10_issues_abiertos', user_get_10_issues_abiertos)
User.add_to_class('get_tareas_activas', user_get_tareas_activas)
User.add_to_class('get_tareas_recientes', user_get_tareas_recientes)
User.add_to_class('get_apikey', user_get_apikey)

# Signals
models.signals.post_save.connect(create_api_key, sender=User)
