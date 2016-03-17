# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from khaleesi.settings import URL_HOST
from tastypie.models import create_api_key
from django.contrib.auth.models import User
from track.models import *

@receiver(post_save, sender=issue)
def send_update(sender, instance, **kwargs):
    subject = u'Khaleesi: {0} {1} {2}'.format(instance.tipo_issue, instance.id, instance.get_status())
    to = None

    if kwargs['created'] and instance.status == 0:
        to = instance.asignado_a
    elif not kwargs['created'] and instance.status != 0:
        to = instance.created_by

    if to:
        c = Context({
            'issue': instance,
            'es_nuevo': kwargs['created'],
            'URL_HOST': URL_HOST
        })
        template_html = get_template('base_email_issue.html')
        html_content = template_html.render(c)

        new_mail = mail()
        new_mail.subject = subject
        new_mail.body = html_content
        new_mail.send_to = to
        new_mail.save()

@receiver(post_save, sender=tarea)
def signal_post_save_tarea(sender, instance, **kwargs):
    subject = u'Khaleesi: {0} {1} {2}'.format("Tarea", instance.id, instance.get_status())
    to = None

    if kwargs['created']: 
        new_pizarron = pizarron(tarea=instance, created_by=instance.created_by)

        to = instance.created_by
        if instance.created_by == instance.responsable:
            new_pizarron.status = 1
        else:
            new_pizarron.status = 0

        new_pizarron.log = u'Tarea {} asignada a {}.'.format(instance.id, instance.responsable.username)
        new_pizarron.save()

    else:
        if instance.get_last_status_number > 3:
            to = instance.created_by
    
    if to:
        c = Context({
            'tarea': instance,
            'es_nuevo': kwargs['created'],
            'URL_HOST': URL_HOST
        })
        template_html = get_template('base_email_tarea.html')
        html_content = template_html.render(c)

        new_mail = mail()
        new_mail.subject = subject
        new_mail.body = html_content
        new_mail.send_to = to
        new_mail.save()
        
models.signals.post_save.connect(create_api_key, sender=User)
