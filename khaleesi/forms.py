# -*- coding: utf-8 -*-
from django.forms import ModelForm
from track.models import UserProfile
from suit.widgets import SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        widgets = {
            'start_time': SuitTimeWidget,
            'end_time': SuitTimeWidget,
            'lunch_time': SuitTimeWidget,
        }
