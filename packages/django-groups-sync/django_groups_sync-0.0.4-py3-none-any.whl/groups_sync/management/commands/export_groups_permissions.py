import json
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Export User Groups with permissions"

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='group name', nargs='*',
            help='A Group name which should only be exported (use "" if there are spaces in Group name).',
        )
        parser.add_argument(
            '--file', dest='file',
            help='Specifies file to which the json output is written.'
        )

    def handle(self, *group_names, verbosity, **options):
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

        permissions_count = defaultdict(int)
        apps_count = defaultdict(set)
        models_count = defaultdict(set)

        ########################################################
        # Prepare data

        groups = Group.objects.prefetch_related('permissions').all()

        if group_names:
            groups = groups.filter(name__in=group_names)

        for g in groups:
            for p in g.permissions.select_related('content_type').all():
                data['groups'][g.name][p.content_type.app_label][p.content_type.model].append(p.codename)

                permissions_count[g.name] += 1
                apps_count[g.name].add(p.content_type.app_label)
                models_count[g.name].add(p.content_type.model)

        # return json.dumps(data, indent=4, sort_keys=True)

        filepath = options.get('file') or settings.GROUP_SYNC_FILENAME

        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

        if verbosity:
            print('Exported groups:')

            for g in data['groups'].keys():
                print(' - {} ({} permissions, {} apps, {} models)'.format(
                    g,
                    permissions_count[g],
                    len(apps_count[g]),
                    len(models_count[g]),
                ))

            print()
            print('Export saved in file "{}"'.format(filepath))

