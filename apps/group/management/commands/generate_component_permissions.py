import json
from django.core.management.base import BaseCommand


fixture_file = './apps/group/fixtures/component_permissions.json'
posm_components = [
    ('aoi', None),
    ('formList', None),
    ('fp', None),
    ('fp-tasks', None),
    ('fp-tiler', None),
    ('fp/_', None),
    ('fp/assets', None),
    ('imagery', None),
    ('omk', None),
    ('omk/data/forms', None),
    ('posm', None),
    ('posm-admin', None),
    ('replication', None),
    ('submission', None),
    ('tiles', None),
    ('view', None),
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fixture = []
        for p_comp, url_pattern in posm_components:
            fixture.append({
                'model': 'group.PosmComponentPermission',
                'fields': {
                    'code': p_comp,
                    # TODO: 'url_pattern': url_pattern or rf'^/{re.escape(p_comp)}(/.*|$)',
                    'url_pattern': url_pattern or rf'^/{p_comp}(/.*|$)',
                }
            })

        with open(fixture_file, 'w') as fp:
            json.dump(fixture, fp, indent=4)
