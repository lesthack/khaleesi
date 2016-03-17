# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied
from track.models import *
from khaleesi.forms import UserProfileForm
from datetime import datetime

def user_profile(request):
    profileView = UserProfile.objects.get(user=request.user)
    saved = None

    if request.method == 'POST':
        profileForm = UserProfileForm(request.user, request.POST, instance=profileView)
        if profileForm.is_valid():
            profileForm.save()
            saved = True
    else:
        profileForm = UserProfileForm(request.user, instance=profileView)

    return render_to_response('profile_form.html', 
        {
            'form': profileForm,
            'saved': saved,
        },
        context_instance = RequestContext(request)
    )

def json_board(request):
    """
        json_board
    """
    json_data = {
        'user': {
            'id': request.user.id,
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        },
        'tasks': [
            {
                'id': t.id,
                'nombre': t.nombre,
                'descripcion': t.descripcion,
                'fecha_inicial': t.fecha_inicial,
                'fecha_final': t.fecha_final,
                'horas_estimadas': t.get_horas_estimadas(),
                'horas_registradas': t.get_horas_reales(),
                'hora_inicial_proceso': t.get_last_log().created_at,
                'status_id': t.get_last_log().status,
                'proyecto': {
                    'id': t.modulo.proyecto.id,
                    'nombre': t.modulo.proyecto.proyecto
                },
                'modulo': {
                    'id': t.modulo.id,
                    'nombre': t.modulo.modulo
                }
            } 
            for t in request.user.get_tareas_activas()
        ],
        'last_tasks': [
            {
                'id': t.id,
                'nombre': t.nombre,
                'descripcion': t.descripcion,
                'fecha_inicial': t.fecha_inicial,
                'fecha_final': t.fecha_final,
                'horas_estimadas': t.get_horas_estimadas(),
                'horas_registradas': t.get_horas_reales(),
                'hora_inicial_proceso': t.get_last_log().created_at,
                'status_id': t.get_last_log().status,
                'proyecto': {
                    'id': t.modulo.proyecto.id,
                    'nombre': t.modulo.proyecto.proyecto
                },
                'modulo': {
                    'id': t.modulo.id,
                    'nombre': t.modulo.modulo
                }
            } 
            for t in request.user.get_tareas_recientes()
        ]
    }
    return JsonResponse(json_data)

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

        for view_tarea in list_tareas.filter(status=0):
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
                                
        if n > 1:
            all_proyectos.append({
                'proyecto': view_proyecto,
                'resume' : {
                    'horas': {
                        'estimadas': horas_estimatadas_totales,
                        'reales': horas_reales_totales,
                    },
                    'periodo': {
                        'inicio': list_tareas.order_by('fecha_inicial').first().fecha_inicial.strftime('%d/%m/%Y %H:%M'),
                        'fin': list_tareas.order_by('-fecha_final').first().fecha_final.strftime('%d/%m/%Y %H:%M')
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

