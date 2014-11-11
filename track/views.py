from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.admin import site
from django.conf.urls import patterns
from django.http import HttpResponse

def my_view(request):
    return HttpResponse("Hello!")

def gantt_view(request):
    return render_to_response(
        'gantt.html', 
        {},
        context_instance=RequestContext(request)
    )

# Urls
def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
            (r'^my_view/$', site.admin_view(my_view)),
            (r'^gantt/$', site.admin_view(gantt_view))
        )
        return my_urls + urls
    return get_urls
