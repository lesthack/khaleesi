from __future__ import unicode_literals

from django.apps import AppConfig

class TrackConfig(AppConfig):
    name = 'track'

    def ready(self):
        import track.signals
