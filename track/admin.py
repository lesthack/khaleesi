# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from track.models import *
import datetime

class proyectoForm(forms.ModelForm):
    class Meta:
        model = proyecto
        exclude = ['created_by', 'deleted','deleted_by','deleted_at']

class proyectoAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'link', 'descripcion', 'activos', 'cancelados', 'created_by', 'created_at', 'deleted', 'deleted_by']
    list_display_links = ['proyecto']
    search_fields = ['proyecto', 'link', 'descripcion', 'created_by__username', 'deleted', 'deleted_by__username']
    list_filter = ['created_at', 'updated_at', 'deleted']
    form = proyectoForm

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

class moduloAdmin(admin.ModelAdmin):
    list_display = ['modulo', 'proyecto_link', 'descripcion', 'issues_resueltos', 'issues_abiertos', 'issues_abandonados', 'issues_cancelados', 'created_by', 'created_at', 'deleted', 'deleted_by']
    list_display_links = ['modulo']
    search_fields = ['modulo', 'descripcion', 'created_by__username', 'deleted', 'deleted_by__username']
    list_filter = ['proyecto__proyecto', 'created_at','updated_at', 'deleted']
    form = moduloForm

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

class tipo_issueForm(forms.ModelForm):
    class Meta:
        model = tipo_issue
        exclude = ['created_by']

class tipo_issueAdmin(admin.ModelAdmin):
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

class issue_notaAdmin(admin.ModelAdmin):
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

class issueAdmin(admin.ModelAdmin):
    list_display = ['id', 'proyecto_link', 'modulo_link', 'tipo_issue', 'status', 'urgencia', 'importancia', 'descripcion', 'asignado_a', 'created_by', 'created_at']
    list_display_links = ['id']
    search_fields = ['id', 'modulo__proyecto__proyecto', 'modulo__modulo', 'tipo_issue__tipo', 'status', 'urgencia', 'importancia', 'asignado_a__username', 'created_by__username', 'updated_by__username']
    ordering = ['status', '-urgencia','-importancia','-created_at']
    list_filter = ['modulo__proyecto__proyecto', 'modulo__modulo', 'status', 'urgencia', 'importancia', 'asignado_a', 'created_by', 'created_at']
    form = issueForm
    
    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            self.actions = None
            self.exclude = []
            readonly_fields = ()

            if obj.asignado_a  == request.user:
                readonly_fields = ('id', 'modulo', 'tipo_issue', 'updated_by', 'created_at', 'updated_at', 'created_by', 'urgencia', 'importancia', 'descripcion', 'asignado_a', 'link')
                if obj.is_closed():
                    readonly_fields = tuple(list(readonly_fields) + ['status'])
            else:        
                readonly_fields = ('id', 'modulo', 'tipo_issue', 'updated_by', 'created_at', 'updated_at', 'created_by', 'urgencia', 'importancia', 'descripcion', 'asignado_a', 'link', 'status')

            return self.readonly_fields + readonly_fields
        elif obj and request.user.is_superuser:
            self.exclude = []
            if not obj.is_closed():
                return self.readonly_fields + ('id', 'created_at', 'updated_at')
            else:
                readonly_fields = ('id', 'modulo', 'tipo_issue', 'urgencia', 'importancia', 'descripcion', 'asignado_a', 'link', 'updated_by', 'created_at', 'updated_at', 'created_by')
                return self.readonly_fields + readonly_fields
        return self.readonly_fields
    
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.change_form_template = 'issue_view_form.html'
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

admin.site.register(proyecto, proyectoAdmin)
admin.site.register(modulo, moduloAdmin)
admin.site.register(tipo_issue, tipo_issueAdmin)
admin.site.register(issue, issueAdmin)
admin.site.register(issue_nota, issue_notaAdmin)
