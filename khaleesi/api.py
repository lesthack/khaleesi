# myapp/api.py
from tastypie.resources import ModelResource
from track.models import *

class IssueResource(ModelResource):
    class Meta:
        queryset = issue.objects.all()
        resource_name = 'issue'
