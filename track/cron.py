# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
from django.db.models import Q
from khaleesi.settings import URL_HOST
from pushbullet import Pushbullet
from pushbullet.errors import InvalidKeyError
from track.models import *
import urllib2
import json

def mail_daily():
    hoy = datetime.now()
    q = cita()
    date_exceptions = ['31/12/2014']

    if hoy.weekday() not in [0,1,2,3,4] or hoy.strftime('%d/%m/%Y') in date_exceptions:
        return False

    for profile in UserProfile.objects.filter(is_email_active=True, user_id=2):
        try:
            c = Context({
                'hoy': hoy,
                'user': profile.user,
                'quote': cita.objects.filter(deleted=False).order_by('?')[0],
                'URL_HOST': URL_HOST
            })
            html_template = get_template('email_daily.html')
            html_content = html_template.render(c)
            new_mail = mail()
            new_mail.subject = 'Actividades {}'.format(hoy.strftime('%B %d, %Y'))
            new_mail.body = html_content
            new_mail.send_to = profile.user
            new_mail.save()
        except Exception, e:
            print 'Error: ',e

    return True

def mail_sending():
    emails_to_send = mail.objects.filter(sended=False,error=False)
    for item in emails_to_send:
        item.send()

def get_url_image():
    meme_api_url = 'http://version1.api.memegenerator.net/Generators_Search?q=geek&pageIndex=0&pageSize=24'
    imageUrl=''
    try:
        data = json.load(urllib2.urlopen(meme_api_url))
        imageUrl = data['result'][random.randint(0,23)]['imageUrl']
        print imageUrl
    except Exception as e:
        print 'Error: ', e
    return imageUrl

def pausetask_listening():
    tareas_list = tarea.objects.raw('SELECT * FROM track_tarea WHERE status=0 AND (SELECT status FROM track_pizarron WHERE tarea_id=track_tarea.id ORDER BY created_at DESC LIMIT 1 OFFSET 0)=2 ORDER BY responsable_id;')
    pb = {}
    for view_tarea in tareas_list:
        new_pizarron = pizarron(tarea=view_tarea)
        new_pizarron.status = 3
        new_pizarron.created_by = view_tarea.created_by
        new_pizarron.save()
        token = view_tarea.created_by.userprofile.token
        if token not in pb.keys():
            pb[token] = Pushbullet(token)
        pb[token].push_note('khaleesi notifications', u'La tarea {} ({}) se ha pausado de forma automática.'.format(view_tarea.id, view_tarea.nombre))

def pushbullet_listening():
    week = ['mon','tue','wed','thu','fri','sat','sun']
    day_of_week = week[datetime.today().weekday()]
    hour_of_day = datetime.now().hour
    minute_of_day = datetime.now().minute

    title = 'Khaleesi notifications'
    now_time = '{hour}:{minute}:00'.format(hour=hour_of_day, minute=minute_of_day)

    list_notifications = {
        'start_time': {
            'text': 'Buen día. Es hora de comenzar a trabajar. No olvides activar tus tareas.',
            'filter': {'start_time': now_time},
            'type': 'note'
         },
        'lunch_time': {
            'text': 'Hora de comer ! Recuerda pausar tus tareas activas.',
            'filter': {'lunch_time': now_time},
            'type': 'image'
         },
        'end_time': {
            'text': 'Tu día parece haber terminado. Buen trabajo. Recuerda que a las 6pm todas las tareas activas se pausarán automáticamente.',
            'filter': {'end_time': now_time},
            'type': 'link',
            'url': 'http://khaleesi.unisem.mx/admin/track/tarea/'
         }
    }

    for profile in UserProfile.objects.filter(Q(**{day_of_week: True}) & Q(token__isnull=False)):
        try:
            pb = Pushbullet(profile.token)
            print profile.user
            for notification in list_notifications.keys():
                if UserProfile.objects.filter(id=profile.id).filter(Q(**list_notifications[notification]['filter'])).count() > 0:
                    if list_notifications[notification]['type'] == 'note':
                        push = pb.push_note(title, list_notifications[notification]['text'])
                    elif list_notifications[notification]['type'] == 'link':
                        push = pb.push_link(title, url=list_notifications[notification]['url'], body=list_notifications[notification]['text'])
                    elif list_notifications[notification]['type'] == 'image':
                        push = pb.push_file(file_url=get_url_image(), file_name=title, file_type='image/jpeg', body=list_notifications[notification]['text'])
                    print push
        except Exception as e:
            print 'Error: ', e        
