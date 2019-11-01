import json
from django.core.management.base import BaseCommand


fixture_file = './apps/group/fixtures/component_permissions.json'

# This are defined in POSM nginx config (sample /posn-nginx/posm.conf)
posm_components = [
    'aoi',
    'formList',
    'fp',
    'fp-tasks',
    'fp-tiler',
    'fp-_',
    'fp-assets',
    'imagery',
    'omk',
    'omk-data-forms',
    'posm',
    'posm-admin',
    'replication',
    'submission',
    'tiles',
    'view',
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fixture = []
        for p_comp in posm_components:
            fixture.append({
                'model': 'group.PosmComponentPermission',
                'fields': {
                    'code': p_comp,
                }
            })

        with open(fixture_file, 'w') as fp:
            json.dump(fixture, fp, indent=4)
