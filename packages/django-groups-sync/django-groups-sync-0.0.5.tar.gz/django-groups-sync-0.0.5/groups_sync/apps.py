from django.apps import AppConfig


class GroupsSyncConfig(AppConfig):
    name = 'groups_sync'

    def ready(self):
        from django.conf import settings

        settings = settings._wrapped.__dict__

        settings.setdefault('GROUP_SYNC_FILENAME', 'groups_permissions.json')
