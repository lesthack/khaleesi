from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from track.models import *

@receiver(post_save, sender=issue)
def send_update(sender, instance, created, **kwargs):
    STATUS_CHOICES = (
        (0, 'Abierto'),
        (1, 'Resuelto'),
        (2, 'Abandonado'),
        (3, 'Cancelado')
    )
    message = 'http://khaleesi.unisem.mx/admin/track/issue/{0}/'.format(instance.id)
    subject = 'Khaleesi: {0} {1} {2}'.format(instance.tipo_issue, instance.id, STATUS_CHOICES[instance.status][1])
    
    if instance.status == 0:
        to = instance.asignado_a.email
    else:
        to = instance.created_by.email

    send_mail(subject, message, 'khaleesi@maices.com', [to,])

@receiver(post_save, sender=tarea)
def signal_post_save_tarea(sender, instance, **kwargs):
    if kwargs['created']: # Si es nuevo
        new_pizarron = pizarron(tarea=instance, created_by=instance.created_by)
    
        if instance.created_by == instance.responsable:
            new_pizarron.status = 1
        else:
            new_pizarron.status = 0

        new_pizarron.log = u'Tarea {} asginada a {}.'.format(instance.id, instance.created_by.username)
        new_pizarron.save()

#post_save.connect(send_update, sender=issue)
