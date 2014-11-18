# -*- coding: utf-8 -*-
from track.models import *

def mail_sending():
    print 'Pasa por mail_sending'
    emails_to_send = mail.objects.filter(sended=False,error=False)
    for item in emails_to_send:
        item.send()
