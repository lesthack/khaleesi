from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.admin import site
from django.conf.urls import patterns
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from track.models import *
import random

def my_view(request):
    return render_to_response(
        'base_email_issue.html', 
        {
            'issue': issue.objects.get(id=221),
            'es_nuevo': False
        },
        context_instance=RequestContext(request)
    )

def generate_gantt_filter(proyecto_id=None, user_id=None, terminadas=True):
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
        horas_estimatadas_totales = 0
        horas_reales_totales = 0
        numero_tareas_totales = list_tareas.count()
        total_tareas = {0:0, 1:0, 2:0, 3:0, 4: 0, 5:0, 6:0, 7:0}
        involucrados = []

        # Solo tareas abiertas
        list_tareas = list_tareas.filter(status=0)

        for view_tarea in list_tareas:
            # Para no afectar a google en el diagrama de Gantt
            if view_tarea.fecha_inicial >= view_tarea.fecha_final:
                continue

            horas_estimatadas_totales += view_tarea.get_horas_estimadas()
            horas_reales_totales += view_tarea.get_horas_reales()
            total_tareas[view_tarea.get_last_log().status] += 1

            if view_tarea.responsable not in involucrados:
                involucrados.append(view_tarea.responsable)

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
        
        n = len(rows)
        
        print total_tareas

        if n > 1:
            all_proyectos.append({
                'proyecto': view_proyecto,
                'resume' : {
                    'horas': {
                        'estimadas': horas_estimatadas_totales,
                        'reales': horas_reales_totales,
                    },
                    'periodo': {
                        'inicio': list_tareas[0].created_at.strftime('%d/%m/%Y %H:%M'),
                        'fin': list_tareas[n-1].created_at.strftime('%d/%m/%Y %H:%M')
                    },
                    'tareas': {
                        'totales': numero_tareas_totales,
                        'terminadas': numero_tareas_totales-n,
                        'pendientes': total_tareas[1],
                        'proceso': total_tareas[2],
                        'pausadas': total_tareas[3],
                        'bloqueadas': total_tareas[5],
                        'asignadas': total_tareas[0],
                        'abandonadas': total_tareas[7]
                    },
                    'involucrados': involucrados
                 },
                'rows': rows,
                'colors': colors,
                'height': 75*n
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

def gantt_por_usuario(request, user_id):
    proyectos = generate_gantt_filter(user_id=user_id)
    return render_to_response(
        'gantt.html', 
        {
            'proyectos': proyectos,
        },
        context_instance=RequestContext(request)
    )

def gantt_por_usuario_proyecto(request, user_id, proyecto_id):
    proyectos = generate_gantt_filter(proyecto_id=proyecto_id, user_id=user_id)
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

def board(request, tarea_id, status_id):
    try:
        view_tarea = tarea.objects.get(id=tarea_id)
        if view_tarea.responsable != request.user or status_id in [6, 7]:
            raise PermissionDenied
        new_pizarron = pizarron(tarea=view_tarea)
        new_pizarron.status = int(status_id)
        new_pizarron.created_by = request.user
        new_pizarron.save()
    except IndexError:
        pass
    except tarea.DoesNotExist:
        return HttpResponseRedirect('/admin/track/tarea/')
    return HttpResponseRedirect('/admin/track/tarea/{0}/'.format(tarea_id))

# Urls
def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
            (r'^my_view/$', site.admin_view(my_view)),
            (r'^gantt/$', site.admin_view(gantt_all)),
            (r'^track/proyecto/(?P<proyecto_id>\d+)/gantt/$', site.admin_view(gantt_por_proyecto)),
            (r'^track/user/(?P<user_id>\d+)/gantt/$', site.admin_view(gantt_por_usuario)),
            (r'^track/user/(?P<user_id>\d+)/proyecto/(?P<proyecto_id>\d+)/gantt/$', site.admin_view(gantt_por_usuario_proyecto)),
            (r'^track/tarea/(?P<tarea_id>\d+)/board/(?P<status_id>\d+)/$', site.admin_view(board)),
        )
        return my_urls + urls
    return get_urls
