import logging
import base64
from rest_framework import test, status

from group.models import User, PosmComponentPermission
from group.management.commands.generate_component_permissions import posm_components

logger = logging.getLogger(__name__)


class GroupTest(test.APITestCase):
    fixtures = ('component_permissions.json',)

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
        for module in posm_components:
            user.profile.permissions.all().delete()
            user.profile.permissions.add(PosmComponentPermission.objects.get(code=module))

            for _module in posm_components:
                response = self.client.get('/permission-validate/', **{'HTTP_X-POSM-AUTH-MODULE': _module})
                expected_status_code = status.HTTP_200_OK if _module == module else status.HTTP_403_FORBIDDEN
                assert response.status_code == expected_status_code,\
                    f'Response code should be {expected_status_code} with module permission: {module} for module: {_module}'
