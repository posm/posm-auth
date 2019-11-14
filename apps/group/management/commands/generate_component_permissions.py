import json
from django.core.management.base import BaseCommand


fixture_file = './apps/group/fixtures/component_permissions.json'

# This are defined in POSM nginx config (sample /posn-nginx/posm.conf)
posm_components = [
    # Code, Name, Description
    ('omk', 'OpenMapKit', None),
    ('fp', 'Field Papers', None),
    ('osm', 'OpenStreetMap', None),
    ('odmgcp', 'ODM GCPs', 'OpenDroneMap Ground Control Points'),
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fixture = []
        for p_comp, name, description in posm_components:
            fixture.append({
                'model': 'group.PosmComponentPermission',
                'fields': {
                    'code': p_comp,
                    'name': name,
                    'description': description,
                }
            })

        with open(fixture_file, 'w') as fp:
            json.dump(fixture, fp, indent=4)
