# myapp/api.py
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from track.models import *

class IssueResource(ModelResource):
    class Meta:
        queryset = issue.objects.all()
        resource_name = 'issue'
        authentication = ApiKeyAuthentication()

    def get_object_list(self, request):
        return super(IssueResource, self).get_object_list(request).filter(asignado_a=request.user)

class TareaResource(ModelResource):
    class Meta:
        queryset = tarea.objects.all()
        resource_name = 'tarea'
        authentication = ApiKeyAuthentication()

    def get_object_list(self, request):
        return super(TareaResource, self).get_object_list(request).filter(responsable=request.user)

class PizarronResource(ModelResource):
    class Meta:
        queryset = pizarron.objects.all()
        resource_name = 'pizarron'
        authentication = ApiKeyAuthentication()

    def get_object_list(self, request):
        return super(PizarronResource, self).get_object_list(request).filter(created_by=request.user)

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'username', 'first_name', 'last_name']
        authentication = ApiKeyAuthentication()
    
    def get_object_list(self, request):
        glist = super(UserResource, self).get_object_list(request)
        if not request.user.is_superuser:
            glist = glist.filter(id=request.user.id)
        return glist

