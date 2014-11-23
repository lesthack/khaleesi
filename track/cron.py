# -*- coding: utf-8 -*-
from track.models import *
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
import random

def mail_daily():
    for user in User.objects.filter(id=2):
        hoy = datetime.now()
        try:
            c = Context({
                'hoy': hoy,
                'user': user,
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

def mail_sending():
    emails_to_send = mail.objects.filter(sended=False,error=False)
    for item in emails_to_send:
        item.send()
