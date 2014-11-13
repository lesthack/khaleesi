# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from track.models import *

@receiver(post_save, sender=issue)
def send_update(sender, instance, **kwargs):
    url = 'http://khaleesi.unisem.mx/admin/track/issue/{0}/'.format(instance.id)
    subject = u'Khaleesi: {0} {1} {2}'.format(instance.tipo_issue, instance.id, instance.get_status())
    message = ''
    to = None
    if kwargs['created'] and instance.status == 0:
        message = u'El usuario {} te ha asignado un nuevo issue. \n\nDescripción: \n\n\t{} \n\nPuedes ver mas detalles en el siguiente enlace. \n{}.'.format(instance.created_by.username, instance.descripcion, url)
        to = instance.asignado_a.email
    elif not kwargs['created'] and instance.status != 0 and instance.asignado_a != instance.created_by:
        message = u'El usuario {} ha {} el issue que le asignaste. \n\nDescripción: \n\n\t{} \n\nPuedes ver mas detalles en el siguiente enlace. \n{}.'.format(instance.asignado_a.username, instance.get_status(), instance.descripcion, url)
        to = instance.created_by.email
    if to:
        send_mail(subject, message, 'support@koalaideas.com', [to,])

@receiver(post_save, sender=tarea)
def signal_post_save_tarea(sender, instance, **kwargs):
    if kwargs['created']: # Si es nuevo
        new_pizarron = pizarron(tarea=instance, created_by=instance.created_by)
    
        if instance.created_by == instance.responsable:
            new_pizarron.status = 1
        else:
            new_pizarron.status = 0

        new_pizarron.log = u'Tarea {} asginada a {}.'.format(instance.id, instance.responsable.username)
        new_pizarron.save()
