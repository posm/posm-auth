import logging
import base64
from rest_framework import test, status

from group.models import User, PosmComponentPermission
from group.management.commands.generate_component_permissions import posm_components

logger = logging.getLogger(__name__)


class GroupTest(test.APITestCase):
    fixtures = ('component_permissions.json',)
    test_urls = {
        module: [
            template.format(module)
            for template in (
                '/{0}',
                '/{0}/',
                '/{0}/random-path',
                '/{0}/random-path?random-params=random-values',
                '/{0}/random-another-path/random-text?random-params=random-values',
            )
        ]
        for module, _ in posm_components
    }

    def setUp(self):
        self.root_user = User.objects.create_user(
            username='root',
            first_name='Root',
            last_name='Toot',
            password='admin123',
            is_superuser=True,
            is_staff=True,
        )
        self.user = User.objects.create_user(
            username='normal',
            first_name='Normal',
            last_name='Toot',
            password='admin123',
        )

    def authenticate(self, username, password):
        self.client.credentials(
            HTTP_AUTHORIZATION='Basic ' + base64.b64encode(f'{username}:{password}'.encode()).decode()
        )

    def test_permission(self):
        self.authenticate('normal', 'admin123')
        user = self.user
        for module, _ in posm_components:
            user.profile.permissions.all().delete()
            user.profile.permissions.add(PosmComponentPermission.objects.get(code=module))

            for url_module, urls in self.test_urls.items():
                for url in urls:
                    response = self.client.get('/permission-validate/', **{'HTTP_X-Original-URI': url})
                    expected_status_code = status.HTTP_200_OK if url_module == module else status.HTTP_403_FORBIDDEN
                    assert response.status_code == expected_status_code,\
                        f'Response code should be {expected_status_code} for module: {module} with url: {url_module}:{url}'
