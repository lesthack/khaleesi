# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView
from django.contrib.admin import site
from django.contrib import admin
#from tastypie.api import Api
from track.views import *
from api import *

#admin.autodiscover()

#v1_api = Api(api_name='v1')
#v1_api.register(IssueResource())
#v1_api.register(TareaResource())
#v1_api.register(PizarronResource())
#v1_api.register(UserResource())

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/admin')),
    #url(r'^api/', include(v1_api.urls)),
    url(r'^admin/resume/$', site.admin_view(resume)),
    url(r'^admin/gantt/$', site.admin_view(gantt_all)),
    url(r'^admin/json/board/$', site.admin_view(json_board)),
    url(r'^admin/auth/profile/$', site.admin_view(user_profile), name='user_profile'),
    url(r'^admin/track/proyecto/(?P<proyecto_id>\d+)/gantt/$', site.admin_view(gantt_por_proyecto)),
    url(r'^admin/track/user/(?P<user_id>\d+)/gantt/$', site.admin_view(gantt_por_usuario)),
    url(r'^admin/track/user/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/gantt/$', site.admin_view(gantt_por_usuario_proyecto)),
    url(r'^admin/track/tarea/(?P<tarea_id>\d+)/board/(?P<status_id>\d+)/$', site.admin_view(board)),
    url(r'^admin/track/tarea/(?P<tarea_id>\d+)/change/board/(?P<status_id>\d+)/$', site.admin_view(board)),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
]
