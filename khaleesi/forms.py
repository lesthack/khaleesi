# -*- coding: utf-8 -*-
from django.forms import *
from track.models import UserProfile
from django.contrib.admin import widgets

class UserProfileForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = UserProfile
        exclude = ['user']
        widgets = {
            'start_time': TextInput(attrs={'type':'time'}),
            'end_time': TextInput(attrs={'type':'time'}),
            'lunch_time': TextInput(attrs={'type':'time'}),
            'token': TextInput(attrs={'style':'width: 100%'})
        }

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
    
        if not self.user.is_superuser:
            cleaned_data['show_resume'] = self.instance.show_resume

        return cleaned_data
