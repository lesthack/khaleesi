# -*- coding: utf-8 -*-
from django.forms import ModelForm
from track.models import UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
