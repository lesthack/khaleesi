# myapp/api.py
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from track.models import *
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

class IssueResource(ModelResource):
    class Meta:
        queryset = issue.objects.all()
        resource_name = 'issue'
        authentication = ApiKeyAuthentication()

    def get_object_list(self, request):
        return super(IssueResource, self).get_object_list(request).filter(asignado_a=request.user)

class TareaResource(ModelResource):
    pizarron_status = fields.CharField(attribute='pizarron_status', null=True)
    horas_reales = fields.CharField(attribute='horas_reales', null=True)

    class Meta:
        queryset = tarea.objects.all()
        resource_name = 'tarea'
        authentication = ApiKeyAuthentication()

    def get_object_list(self, request):
        return super(TareaResource, self).get_object_list(request).filter(responsable=request.user)

    def dehydrate(self, bundle):
        bundle.data['pizarron_status'] = bundle.obj.get_last_status_number()
        bundle.data['horas_reales'] = bundle.obj.get_horas_reales()
        return bundle

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'first_name', 'last_name']
        authentication = ApiKeyAuthentication()
    
    def get_object_list(self, request):
        glist = super(UserResource, self).get_object_list(request)
        if not request.user.is_superuser:
            glist = glist.filter(id=request.user.id)
        return glist

class PizarronResource(ModelResource):
    tarea = fields.ForeignKey(TareaResource, 'tarea')
    created_by = fields.ForeignKey(UserResource, 'created_by')

    class Meta:
        queryset = pizarron.objects.all()
        resource_name = 'pizarron'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post']
        fields = ['status', 'tarea', 'created_by']

    def get_object_list(self, request):
        return super(PizarronResource, self).get_object_list(request).filter(created_by=request.user)
