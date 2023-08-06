from django.conf import settings

settings.GROUP_SYNC_FILENAME = getattr(settings, 'GROUP_SYNC_FILENAME', 'groups_perms.json')
