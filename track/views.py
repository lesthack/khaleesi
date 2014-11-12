from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.admin import site
from django.conf.urls import patterns
from django.http import HttpResponse
from track.models import *
import random

def my_view(request):
    return HttpResponse("Hello!")

def generate_gantt_filter(proyecto_id=None, user_id=None, terminadas=False):
    """
        Gantt por proyecto
        Gantt por usuario
        Gannt por proyecto y usuario
    """
    all_proyectos = []

    list_proyectos = proyecto.objects.all()
    
    if proyecto_id:
        list_proyectos = list_proyectos.filter(id=proyecto_id)

    for view_proyecto in list_proyectos:
        list_tareas = tarea.objects.filter(modulo__proyecto=view_proyecto).order_by('fecha_inicial', 'fecha_final')
        
        if user_id:
            list_tareas = list_tareas.filter(responsable_id=user_id)
        
        rows = []
        colors = []
        for view_tarea in list_tareas:
            if not terminadas and view_tarea.get_last_log().status == 4: 
                continue
            row = {
                'modulo': view_tarea.modulo.modulo, 
                'tarea': u'[{1}] {0} - {2} - Estimadas: {3}hrs - Reales: {4}hrs'.format(view_tarea.nombre, view_tarea.responsable, view_tarea.get_last_status(), view_tarea.get_horas_estimadas(), view_tarea.get_horas_reales()), 
                'fecha_inicial': {
                    'year':  view_tarea.fecha_inicial.year, 
                    'month': view_tarea.fecha_inicial.month, 
                    'day':   view_tarea.fecha_inicial.day,
                },
                'fecha_final': {
                    'year':  view_tarea.fecha_final.year, 
                    'month': view_tarea.fecha_final.month, 
                    'day':   view_tarea.fecha_final.day,
                },
            }
            rows.append(row)
            colors.append(view_tarea.get_color_status())
        
        if len(rows) > 1:
            all_proyectos.append({
                'proyecto': view_proyecto,
                'rows': rows,
                'colors': colors,
                'height': 75*len(rows)
            })

    return all_proyectos

def gantt_por_proyecto(request, proyecto_id):
    proyectos = generate_gantt_filter(proyecto_id=proyecto_id)
    return render_to_response(
        'gantt.html', 
        {
            'proyectos': proyectos,
        },
        context_instance=RequestContext(request)
    )

def gantt_all(request):
    proyectos = generate_gantt_filter(terminadas=True)
    return render_to_response(
        'gantt.html', 
        {
            'proyectos': proyectos,
        },
        context_instance=RequestContext(request)
    )

# Urls
def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
            (r'^my_view/$', site.admin_view(my_view)),
            (r'^gantt/$', site.admin_view(gantt_all)),
            (r'^track/proyecto/(?P<proyecto_id>\d+)/gantt/$', site.admin_view(gantt_por_proyecto)),
        )
        return my_urls + urls
    return get_urls
