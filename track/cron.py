# -*- coding: utf-8 -*-
from track.models import *
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
from track.quotes import *

def mail_daily():
    hoy = datetime.now()
    date_exceptions = ['31/12/2014']
    list_users = [
        2, # jorgeluis
        4, # edgar
        5, # luis
        6, # diana
    ]

    if hoy.weekday() not in [0,1,2,3,4] or hoy.strftime('%d/%m/%Y') in date_exceptions:
        return False

    for user in User.objects.filter(id__in=list_users):
        try:
            c = Context({
                'hoy': hoy,
                'user': user,
                'quote': random_quote(),
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
