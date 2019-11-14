import logging
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.db.models import Q
from django.conf import settings

from rest_framework import views, response, status

from .models import PosmComponentPermission
from .serializers import PosmComponentPermissionSerializer

logger = logging.getLogger(__name__)


class UnauthorizedResponse(response.Response):
    status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenResponse(response.Response):
    status_code = status.HTTP_403_FORBIDDEN


class SuccessfulResponse(response.Response):
    status_code = status.HTTP_200_OK


class LoginView(auth_views.LoginView):
    template_name = 'posm/login.html'
    redirect_field_name = 'next'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        """NOTE: To accept any redirect urls without success_url_allowed_hosts"""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        return redirect_to


class AssignedPermissionListView(views.APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return UnauthorizedResponse()

        permissions = PosmComponentPermission.objects.filter(
            Q(usergroup__members=request.user) | Q(profile__user=request.user)
        ).distinct()

        return response.Response(
            PosmComponentPermissionSerializer(permissions, many=True).data
        )


class PermissionValidationView(views.APIView):
    def get(self, request):
        # NOTE: Not using permissions.IsAuthenticated since it's response is 403 instead of 401
        if request.user.is_anonymous:
            return UnauthorizedResponse()

        # NOTE: If X-POSM-AUTH-MODULE is not provided then it will be treated as public for authenticated users
        module = request.headers.get('X-POSM-AUTH-MODULE', 'public')

        # NOTE: Superuser have all access, 'public' module are accessable to all authenticated users
        if request.user.is_superuser or module == 'public' or (
                PosmComponentPermission.objects.filter(
                    Q(usergroup__members=request.user) | Q(profile__user=request.user),
                    code=module,
                ).exists()
        ):
            return SuccessfulResponse()
        return ForbiddenResponse()


class Error400(TemplateView):
    def get_template_names(self):
        error = self.request.path.replace('/', '')
        if error == '403':
            return 'posm/403.html'
        return 'posm/404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'home_url': settings.POSM_ADMIN_URL,
        })
        return context


class DummyView(TemplateView):
    template_name = 'posm/dummy_page.html'
