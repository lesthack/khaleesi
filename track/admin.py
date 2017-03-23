# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from track.models import *
from khaleesi.hacks import *
import datetime

class proyectoForm(forms.ModelForm):
    class Meta:
        model = proyecto
        exclude = ['created_by', 'deleted', 'deleted_by', 'deleted_at']

@admin.register(proyecto)
class proyectoAdmin(nModelAdmin):
    list_display = ['proyecto', 'link_short', 'descripcion', 'activos', 'cancelados', 'gantt_link', 'created_by', 'created_at_simple']
    list_display_links = ['proyecto']
    list_display_mobile = ['proyecto', 'link_short', 'activos', 'cancelados']
    search_fields = ['proyecto', 'link', 'descripcion', 'created_by__username']
    list_filter = ['created_at', 'updated_at', 'deleted']
    form = proyectoForm
    actions_on_bottom = True
    actions_on_top = False

    def get_queryset(self, request):
        qs = super(proyectoAdmin, self).get_queryset(request).filter(deleted=False)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if request.user.is_superuser or obj.created_by==request.user:
                self.exclude = ['created_by', 'deleted_by', 'deleted_at', 'deleted']
            elif not request.user.is_superuser:
                return self.readonly_fields + ('proyecto', 'descripcion', 'link', 'created_by', 'created_at', 'deleted', 'deleted_at', 'deleted_by')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if change:
            if obj.deleted == False:
                obj.deleted_by = None
                obj.deleted_at = None
        else:
            obj.created_by = request.user
        obj.save()
    
    def delete_model(self, request, obj):
        obj.deleted = True
        obj.deleted_by = request.user
        obj.deleted_at = datetime.datetime.now()
        obj.save()
        return False


class moduloForm(forms.ModelForm):
    class Meta:
        model = modulo
        exclude = ['created_by', 'deleted', 'deleted_by', 'deleted_at']

@admin.register(modulo)
class moduloAdmin(nModelAdmin):
    list_display = ['proyecto_link', 'modulo', 'descripcion', 'issues_resueltos', 'issues_abiertos', 'issues_abandonados', 'issues_cancelados', 'created_by', 'created_at_simple']
    list_display_links = ['modulo']
    list_display_mobile = ['modulo', 'proyecto_link', 'issues_abiertos']
    search_fields = ['modulo', 'descripcion', 'created_by__username', 'deleted', 'deleted_by__username']
    list_filter = ['proyecto__proyecto', 'created_at','updated_at', 'deleted']
    ordering = ('proyecto__proyecto', 'modulo')
    form = moduloForm
    list_per_page = 10

    def get_queryset(self, request):
        qs = super(moduloAdmin, self).get_queryset(request).filter(deleted=False)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.created_by != request.user:
                return self.readonly_fields + ('proyecto', 'modulo', 'descripcion', 'created_by', 'created_at', 'deleted', 'deleted_at', 'deleted_by')
            if request.user.is_superuser:
                self.exclude = ['created_by', 'deleted_by', 'deleted_at']
                return self.readonly_fields + ('deleted_at', 'deleted_by', 'created_by', 'created_at')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if change:
            if obj.deleted == False:
                obj.deleted_by = None
                obj.deleted_at = None
        else:
            obj.created_by = request.user
        obj.save()
    
    def delete_model(self, request, obj):
        obj.deleted = True
        obj.deleted_by = request.user
        obj.deleted_at = datetime.datetime.now()
        obj.save()

        return False

class tareaForm(forms.ModelForm):    
    class Meta:
        model = tarea
        exclude = ['created_by', 'created_at', 'updated_at', 'status']

    def clean(self):
        cleaned_data = super(tareaForm, self).clean()

        if cleaned_data.get("fecha_inicial") >= cleaned_data.get("fecha_final"):
            msg = u'La fecha final debe ser mayor a la fecha inicial.'
            self._errors["fecha_final"] = self.error_class([msg])

        return cleaned_data

@admin.register(tarea)
class tareaAdmin(nModelAdmin):
    list_display = ['id', 'proyecto_link', 'nombre', 'periodo', 'get_horas_estimadas', 'admin_horas_reales', 'get_pizarron', 'responsable_link', 'created_by', 'created_at_simple']
    list_display_links = ['id', 'nombre']
    list_display_mobile = ['id', 'nombre']
    search_fields = ['nombre', 'descripcion', 'responsable__username']
    list_filter = ['modulo__proyecto__proyecto', 'status', 'responsable', 'fecha_inicial', 'fecha_final']
    actions = None
    form = tareaForm
    list_per_page = 10

    def admin_horas_reales(self, obj):
        return '%.2f' % round(obj.get_horas_reales(), 2)
    admin_horas_reales.allow_tags = True
    admin_horas_reales.short_description = 'Hrs Rls.'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            if obj.responsable is None:
                obj.responsable = obj.created_by
            obj.save() # and trigger signal
        elif request.user == obj.responsable and not obj.fecha_inicial is None and not obj.fecha_final is None and not obj.horas_estimadas is None and obj.get_last_log().status == 0:
            obj.save()
            new_pizarron = pizarron(tarea=obj, created_by=obj.responsable)
            new_pizarron.status = 1
            new_pizarron.log = u'Tarea {} aceptada por {}.'.format(obj.id, obj.responsable)
            new_pizarron.save()
        else:
            print '[admin_track_tarea] Alguien trata de guardar una tarea que bien, no es de él, o ya no es posible editar.'

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 0: # Si aun esta abierto
            self.exclude = ['created_by', 'created_at', 'updated_at', 'status']
            if obj.get_last_log().status == 0 and obj.responsable == request.user:
                if obj.fecha_inicial is None or obj.fecha_final is None or obj.horas_estimadas is None:
                    return self.readonly_fields + ('modulo', 'nombre', 'descripcion', 'responsable', 'status')
            self.actions = None
            return self.readonly_fields + ('modulo', 'nombre', 'descripcion', 'responsable', 'fecha_inicial', 'fecha_final', 'horas_estimadas', 'status')
        elif obj and obj.status == 1:
            return self.readonly_fields + ('modulo', 'nombre', 'descripcion', 'responsable', 'fecha_inicial', 'fecha_final', 'horas_estimadas', 'status')
        return self.readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.change_form_template = 'tarea_view_form.html'
        return super(tareaAdmin, self).get_form(request, obj, **kwargs)

    def changelist_view(self, request, extra_context=None):
        q = request.GET.copy()
        if not request.GET.has_key('status__exact'):
            q['status__exact'] = '0'            
        if not request.GET.has_key('responsable__id__exact'):
            q['responsable__id__exact'] = '{}'.format(request.user.id)
        request.GET = q
        request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(tareaAdmin,self).changelist_view(request, extra_context=extra_context)

@admin.register(pizarron)
class pizarronAdmin(nModelAdmin):
    list_display = ['id', 'responsable_link', 'proyecto_link', 'modulo_link', 'tarea_link', 'status', 'log', 'created_at']
    list_display_links = ['id']
    list_display_mobile = ['id', 'tarea_link', 'status']
    search_fields = ['log']
    list_filter = ['tarea__modulo__proyecto__proyecto', 'tarea__modulo__modulo', 'tarea__responsable__username', 'status']
    exclude = ['created_by', 'log']
    ordering = ['-created_at']
    actions = None

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('tarea', 'log', 'status', 'created_by', 'created_at', 'updated_at')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            #if obj.status > 1:
            #    obj.log = '{} ha marcado esta tarea como {}'.format(request.user, obj.get_status())
            obj.save() # and trigger signal

class tipo_issueForm(forms.ModelForm):
    class Meta:
        model = tipo_issue
        exclude = ['created_by']

@admin.register(tipo_issue)
class tipo_issueAdmin(nModelAdmin):
    list_display = ['tipo', 'created_by', 'created_at']
    list_display_links = ['tipo']
    search_fields = ['tipo']
    list_filter = ['created_at','updated_at']
    form = tipo_issueForm

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

class issue_notaForm(forms.ModelForm):
    class Meta:
        model = issue
        exclude = ['created_by']

@admin.register(issue_nota)
class issue_notaAdmin(nModelAdmin):
    list_display = ['id', 'issue', 'nota', 'like', 'created_by', 'created_at']
    list_display_links = ['id']
    search_fields = ['id', 'issue__id', 'nota', 'issue__modulo__modulo', 'issue__modulo__proyecto__proyecto']
    list_filter = ['created_at', 'updated_at', 'like', 'created_by']
    view_on_site = False
    form = issue_notaForm

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

class NotaInline(admin.StackedInline):
    model = issue_nota
    extra = 1

class issueForm(forms.ModelForm):
    class Meta:
        model = issue
        exclude = ['updated_by', 'created_by', 'created_at', 'updated_at', 'status']

@admin.register(issue)
class issueAdmin(nModelAdmin):
    list_display = ['id', 'proyecto_link', 'modulo_link', 'tipo_issue', 'status', 'urgencia', 'importancia', 'get_descripcion', 'asignado_a', 'created_by', 'created_at_simple']
    list_display_links = ['id', 'get_descripcion']
    list_display_mobile = ['id', 'get_descripcion']
    search_fields = ['id', 'modulo__proyecto__proyecto', 'modulo__modulo', 'tipo_issue__tipo', 'status', 'urgencia', 'importancia', 'asignado_a__username', 'created_by__username', 'updated_by__username']
    ordering = ['status', '-urgencia','-importancia','-created_at']
    list_filter = ['modulo__proyecto__proyecto', 'status', 'asignado_a', 'created_by', 'created_at']
    list_per_page = 10
    form = issueForm
    
    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            self.actions = None
            self.exclude = ()
            readonly_fields = ()

            if obj.asignado_a  == request.user:
                readonly_fields = ('id', 'modulo', 'tipo_issue', 'updated_by', 'created_at', 'updated_at', 'created_by', 'urgencia', 'importancia', 'descripcion', 'asignado_a', 'link')
                if obj.is_closed():
                    readonly_fields = tuple(list(readonly_fields) + ['status'])
            else:        
                readonly_fields = ('id', 'modulo', 'tipo_issue', 'updated_by', 'created_at', 'updated_at', 'created_by', 'urgencia', 'importancia', 'descripcion', 'asignado_a', 'link', 'status')

            return self.readonly_fields + readonly_fields
        elif obj and request.user.is_superuser:
            if not obj.is_closed():
                return self.readonly_fields + ('id', 'created_at', 'updated_at')
            else:
                readonly_fields = ('id', 'modulo', 'tipo_issue', 'urgencia', 'importancia', 'descripcion', 'asignado_a', 'link', 'updated_by', 'created_at', 'updated_at', 'created_by')
                return self.readonly_fields + readonly_fields
        return self.readonly_fields
    
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.change_form_template = 'issue_view_form.html'
        else:
            self.change_form_template = 'issue_new_form.html'
        return super(issueAdmin, self).get_form(request, obj, **kwargs)
    
    def suit_row_attributes(self, obj, request):
        COLORS = (
            ('info', 'info', 'warning'),
            ('info', 'warning', 'error'),
            ('warning', 'error', 'error'),
        )

        if not obj.is_closed():
            row_class = COLORS[obj.urgencia][obj.importancia]
        else:
            row_class = 'success'

        return {'class': row_class, 'data': obj.id}

    def save_model(self, request, obj, form, change):
        if change:
            if 'nota' in request.POST and len(request.POST['nota'].strip())>0:
                new_issue_nota = issue_nota(issue=obj)
                new_issue_nota.nota = request.POST['nota']
                if 'like' in request.POST:
                    new_issue_nota.like = request.POST['like']
                new_issue_nota.created_by = request.user
                new_issue_nota.save()

            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        
        obj.save()

    def changelist_view(self, request, extra_context=None):
        q = request.GET.copy()
        if not request.GET.has_key('status__exact'):
            q['status__exact'] = '0'            
        if not request.GET.has_key('asignado_a__id__exact'):
            q['asignado_a__id__exact'] = '{}'.format(request.user.id)
        request.GET = q
        request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(issueAdmin,self).changelist_view(request, extra_context=extra_context)

class citaForm(forms.ModelForm):
    class Meta:
        model = cita
        exclude = ['created_by','deleted','deleted_by','deleted_at']

@admin.register(cita)
class citaAdmin(nModelAdmin):
    list_display = ['id', 'get_descripcion', 'created_by', 'created_at_simple']
    list_display_links = ['id']
    list_display_mobile = ['id', 'descripcion']
    list_filter = ['created_by', 'created_at']
    search_fields = ['descripcion', 'created_by__username']
    form = citaForm

    def get_queryset(self, request):
        qs = super(citaAdmin, self).get_queryset(request).filter(deleted=False)
        return qs

    def save_model(self, request, obj, form, change):
        obj.save()

    def save_model(self, request, obj, form, change):
        if change:
            if obj.deleted == False:
                obj.deleted_by = None
                obj.deleted_at = None
        else:
            obj.created_by = request.user
        obj.save()
    
    def delete_model(self, request, obj):
        obj.deleted = True
        obj.deleted_by = request.user
        obj.deleted_at = datetime.datetime.now()
        obj.save()

        return False

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Información adicional'
    verbose_name = 'Usuario'

class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'show_resume']
    inlines = (UserProfileInline, )

    def show_resume(self, obj):
        return obj.userprofile.show_resume
    show_resume.short_description = 'Resumen'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
