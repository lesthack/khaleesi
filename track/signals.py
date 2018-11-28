# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from khaleesi.settings import URL_HOST
from django.contrib.auth.models import User
from pushbullet import Pushbullet
from pushbullet.errors import InvalidKeyError
from track.models import *

@receiver(post_save, sender=issue_nota)
def send_nota(sender, instance, **kwrags):
    item_issue = instance.issue
    subject = u'Khaleesi: Nota {0} {1} {2}'.format(item_issue.tipo_issue, item_issue.id, item_issue.get_status())
    to = None

    # Si sigue abierto
    #if item_issue.status == 0:
    if item_issue.created_by == instance.created_by:
        to = item_issue.asignado_a
    else:
        to = item_issue.created_by

    c = Context({
        'nota': instance,
        'URL_HOST': URL_HOST
    })
    template_html = get_template('base_email_nota.html')
    html_content = template_html.render(c)

    new_mail = mail()
    new_mail.subject = subject
    new_mail.body = html_content
    new_mail.send_to = to
    new_mail.save()

@receiver(post_save, sender=issue)
def send_update(sender, instance, **kwargs):
    subject = u'Khaleesi: {0} {1} {2}'.format(instance.tipo_issue, instance.id, instance.get_status())
    to = None

    if kwargs['created'] and instance.status == 0:
        to = instance.asignado_a
    elif not kwargs['created'] and instance.status != 0:
        to = instance.created_by

    if to:
        c = {
            'issue': instance,
            'es_nuevo': kwargs['created'],
            'URL_HOST': URL_HOST
        }
        template_html = get_template('base_email_issue.html')
        html_content = template_html.render(c)

        new_mail = mail()
        new_mail.subject = subject
        new_mail.body = html_content
        new_mail.send_to = to
        new_mail.save()

        try:
            profile = UserProfile.objects.get(user=to)
            if profile.token:
                pb = Pushbullet(profile.token)
                issue_url = 'http://khaleesi.unisem.mx/admin/track/issue/{}/change/'.format(instance.id)
                #push = pb.push_note('Issue {}: {}'.format(instance.id, instance.get_status()), instance.descripcion)
                push = pb.push_link('Issue {}: {}'.format(instance.id, instance.get_status()), url=issue_url, body=instance.descripcion)
                print push
        except Exception as e:
            pass

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
        c = {
            'tarea': instance,
            'es_nuevo': kwargs['created'],
            'URL_HOST': URL_HOST
        }
        template_html = get_template('base_email_tarea.html')
        html_content = template_html.render(c)

        new_mail = mail()
        new_mail.subject = subject
        new_mail.body = html_content
        new_mail.send_to = to
        new_mail.save()
