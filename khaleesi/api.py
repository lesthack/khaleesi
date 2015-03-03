# myapp/api.py
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from track.models import *

class IssueResource(ModelResource):
    class Meta:
        queryset = issue.objects.all()
        resource_name = 'issue'

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['id', 'username', 'first_name', 'last_name']
        # authentication = ApiKeyAuthentication()
