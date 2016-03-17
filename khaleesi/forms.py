# -*- coding: utf-8 -*-
from django.forms import ModelForm
from track.models import UserProfile
from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget

class UserProfileForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = UserProfile
        exclude = ['user']
        widgets = {
            'start_time': SuitTimeWidget,
            'end_time': SuitTimeWidget,
            'lunch_time': SuitTimeWidget,
        }

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
    
        if not self.user.is_superuser:
            cleaned_data['show_resume'] = self.instance.show_resume

        return cleaned_data
