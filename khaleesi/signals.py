from django.db.models.signals import post_save
from django.core.mail import send_mail
from track.models import *

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

post_save.connect(send_update, sender=issue)
