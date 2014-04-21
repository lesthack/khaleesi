# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'khaleesi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(url='/admin')),
    url(r'^admin/', include(admin.site.urls)),
)
