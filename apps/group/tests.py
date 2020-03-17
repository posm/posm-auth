import logging
import mock
from django.db import transaction
from rest_framework import test, status

from group.models import User, PosmComponentPermission
from group.management.commands.generate_component_permissions import posm_components

logger = logging.getLogger(__name__)


class GroupTest(test.APITestCase):
    fixtures = ('component_permissions.json',)

    def run_commit_hooks(self):
        """
        This is to force on_commit and other commit hooks. Because, in testcases,
        those hooks are not run as whole test case is wrapped by outer transaction.

        Source: https://medium.com/gitux/speed-up-django-transaction-hooks-tests-6de4a558ef96
        """
        for db_name in reversed(self._databases_names()):
            with mock.patch(
                    'django.db.backends.base.base.BaseDatabaseWrapper.validate_no_atomic_block',
                    lambda a: False):
                transaction.get_connection(using=db_name).run_and_clear_commit_hooks()

    def setUp(self):
        self.root_user = User.objects.create_user(
            username='root',
            first_name='Root',
            last_name='Toot',
            password='admin123',
            is_superuser=True,
            is_staff=True,
        )
        # User post save has on_commit hook, force it
        self.run_commit_hooks()

        self.user = User.objects.create_user(
            username='normal',
            first_name='Normal',
            last_name='Toot',
            password='admin123',
        )
        # User post save has on_commit hook, force it
        self.run_commit_hooks()

    def authenticate(self, username, password):
        self.client.login(username=username, password=password)

    def test_permission(self):
        self.authenticate('normal', 'admin123')
        user = self.user
        for module, _, _ in posm_components:
            user.profile.permissions.all().delete()
            user.profile.permissions.add(PosmComponentPermission.objects.get(code=module))

            for _module, _, _ in posm_components:
                response = self.client.get('/permission-validate/', **{'HTTP_X-POSM-AUTH-MODULE': _module})
                expected_status_code = status.HTTP_200_OK if _module == module else status.HTTP_403_FORBIDDEN
                assert response.status_code == expected_status_code,\
                    f'Response code should be {expected_status_code} with module permission: {module} for module: {_module}'
