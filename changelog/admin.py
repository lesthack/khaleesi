# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from changelog.models import *
#from suit_redactor.widgets import RedactorWidget
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime

class tipo_datoForm(forms.ModelForm):
    class Meta:
        model = tipo_objeto
        exclude = ['created_by', 'deleted','deleted_by']

class tipo_datoAdmin(admin.ModelAdmin):
    list_display = ['dato', 'created_at', 'updated_at', 'created_by']
    list_display_links = ['dato']
    search_fields = ['dato', 'created_by__username']
    list_filter = ['created_at', 'updated_at']
    view_on_site = False
    form = tipo_datoForm

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

class tipo_objetoForm(forms.ModelForm):
    class Meta:
        model = tipo_objeto
        exclude = ['created_by', 'deleted','deleted_by']

class tipo_objetoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'created_at', 'updated_at', 'created_by']
    list_display_links = ['tipo']
    search_fields = ['tipo', 'created_by__username']
    list_filter = ['created_at', 'updated_at']
    view_on_site = False
    form = tipo_objetoForm

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

class objetoForm(forms.ModelForm):
    nota = forms.Field()
    
    class Meta:
        models = objeto
        #exclude = ['created_by', 'deleted_by']

    def __init__(self, *args, **kwargs):
        super(objetoForm, self).__init__(*args, **kwargs)
        self.fields['nota'] = forms.CharField(label='Nota', widget = forms.Textarea)
        self.fields['nota'].required = False

class objetoAdmin(admin.ModelAdmin):
    list_display = ['objeto', 'relacion_objeto_link', 'tipo_objeto_link', 'tipo_dato_link', 'created_by_link', 'created_at', 'updated_at', 'deleted']
    list_display_links = ['objeto']
    search_fields = ['objeto', 'tipo__tipo', 'tipo_dato__dato', 'created_by__username']
    list_filter = ['tipo', 'relacion_objeto', 'created_at', 'updated_at']
    ordering = ['-created_at']
    form = objetoForm
    fieldsets = [
        ('Objeto', {'fields': ('relacion_objeto','objeto','tipo')}),
        ('Avanzado', {
            'classes': ('collapse',),
            'fields': ('tipo_dato', 'nota', 'deleted')
        }),
    ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        if change:
            old_objeto = objeto.objects.get(id=obj.id)
            obj.save()

            nuevo_cambio = cambio(objeto=obj, tipo_id=2)
            nota = 'Nota de usuario: \n\t{0}\n'.format(form.cleaned_data['nota'].encode('utf8'))
            nota = nota + '\nCambios efectuados:'.format(obj)

            if old_objeto.objeto != obj.objeto:
                nota = nota + '\n\tNombre Anterior: {0}\n\tNombre Actual: {1}'.format(old_objeto.objeto, obj.objeto)
            if old_objeto.relacion_objeto != obj.relacion_objeto:
                nota = nota + '\n\tRelación Anterior: {0}\n\tRelación Actual: {1}'.format(old_objeto.relacion_objeto, obj.relacion_objeto)
            if old_objeto.tipo != obj.tipo:
                nota = nota + '\n\tTipo Anterior: {0}\n\tTipo Actual: {1}'.format(old_objeto.tipo, obj.tipo)
            if old_objeto.deleted == True and obj.deleted == False:
                nota = nota + '\n\tObjeto {0} recuperado.'.format(obj.objeto)
            elif old_objeto.deleted == False and obj.deleted == True:
                nota = nota + '\n\tObjeto {0} eliminado'.format(obj.objeto)
            if old_objeto.tipo_dato != obj.tipo_dato:
                nota = nota + '\n\tTipo Dato Anterior: {0}\n\tTipo Dato Actual: {1}'.format(old_objeto.tipo_dato, obj.tipo_dato)

            nuevo_cambio.nota = nota
            nuevo_cambio.created_by = request.user
            nuevo_cambio.save()
        else:
            obj.save()
            nuevo_cambio = cambio(objeto=obj, tipo_id=1)
            
            if obj.relacion_objeto:
                nuevo_cambio.nota = 'Objeto {0} agregado al objeto {1}.'.format(obj, obj.relacion_objeto)
            else:
                nuevo_cambio.nota = 'Nuevo objeto {0} generado.'.format(obj)
            
            nuevo_cambio.created_by = request.user 
            nuevo_cambio.nota = nuevo_cambio.nota + '\n' + form.cleaned_data['nota'].encode('utf8')
            nuevo_cambio.save()
        
        if obj.deleted:
            obj.deleted_by = request.user
            obj.deleted_at = datetime.datetime.now()
        else:
            obj.deleted_by = None
            obj.deleted_at = None
        
        obj.save()
    
    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse("admin:changelog_cambio_changelist"))

    def delete_model(self, request, obj):
        nuevo_cambio = cambio(objeto=obj, tipo_id=3)
        nuevo_cambio.nota = 'Objeto {0} eliminado.'.format(obj)
        nuevo_cambio.created_by = request.user
        nuevo_cambio.save()

        obj.deleted = True
        obj.deleted_by = request.user
        obj.deleted_at = datetime.datetime.now()
        obj.save()

        return False
    
    def suit_row_attributes(self, obj, request):
        if obj.deleted:
            row_class = 'error'
            return {'class': row_class, 'data': obj.tipo.id}
        return None

class tipo_cambioForm(forms.ModelForm):
    class Meta:
        model = tipo_cambio
        exclude = ['created_by']

class tipo_cambioAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'created_at', 'updated_at', 'created_by']
    list_display_links = ['tipo']
    search_fields = ['tipo', 'created_by__username']
    list_filter = ['created_at', 'updated_at']
    view_on_site = False
    form = tipo_cambioForm

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

class cambioForm(forms.ModelForm):
    class Meta:
        model = cambio
        exclude = ['created_at', 'created_by', 'updated_at']

class cambioAdmin(admin.ModelAdmin):
    list_display = ['id', 'objeto_link', 'tipo_link', 'get_objeto_cambio', 'nota_corta', 'created_by_link', 'created_at', 'updated_at']
    list_display_links = ['id']
    search_fields = ['objeto__objeto', 'tipo__tipo', 'created_by__username', 'objeto__relacion_objeto__objeto']
    list_filter = ['objeto', 'tipo', 'created_by', 'created_at', 'updated_at']
    readonly_fields = ['objeto', 'tipo', 'nota', 'created_by', 'created_at', 'updated_at']
    form = cambioForm

    actions = None
    change_form_template = 'view_form.html'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass
    
    def suit_row_attributes(self, obj, request):
        COLORS = ('info', 'success', 'warning', 'error')
        return {'class': COLORS[obj.tipo.id], 'data': obj.tipo.id}

admin.site.register(tipo_dato, tipo_datoAdmin)
admin.site.register(tipo_objeto, tipo_objetoAdmin)
admin.site.register(tipo_cambio, tipo_cambioAdmin)
admin.site.register(objeto, objetoAdmin)
admin.site.register(cambio, cambioAdmin)
