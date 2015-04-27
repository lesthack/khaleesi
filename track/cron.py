# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
from khaleesi.settings import URL_HOST
from track.models import *

def mail_daily():
    hoy = datetime.now()
    q = cita()
    date_exceptions = ['31/12/2014']
    list_users = UserProfile.objects.filter(is_email_active = 0)

    if hoy.weekday() not in [0,1,2,3,4] or hoy.strftime('%d/%m/%Y') in date_exceptions:
        return False

    for user in User.objects.exclude(id__in=(l.user_id for l in list_users)):
        try:
            c = Context({
                'hoy': hoy,
                'user': user,
                'quote': cita.objects.filter(deleted=False).order_by('?')[0],
                'URL_HOST': URL_HOST
            })
            html_template = get_template('email_daily.html')
            html_content = html_template.render(c)
            new_mail = mail()
            new_mail.subject = 'Actividades {}'.format(hoy.strftime('%B %d, %Y'))
            new_mail.body = html_content
            new_mail.send_to = user
            new_mail.save()
        except Exception, e:
            print 'Error: ',e

    return True

def mail_sending():
    emails_to_send = mail.objects.filter(sended=False,error=False)
    for item in emails_to_send:
        item.send()
