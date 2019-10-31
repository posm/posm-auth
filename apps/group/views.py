import re
from itertools import chain
from rest_framework import views, response, status, permissions
from rest_framework.authentication import BasicAuthentication


class ForbiddenResponse(response.Response):
    status_code = status.HTTP_403_FORBIDDEN


class SuccessfulResponse(response.Response):
    status_code = status.HTTP_200_OK


class PermissionValidationView(views.APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # TODO: Look if this can be cached
    def get(self, request):
        url = request.headers['X-Original-URI']
        print('X-POSM-AUTH-MODULE', request.headers.get('X-POSM-AUTH-MODULE'))
        for url_pattern in set(
            chain(
                request.user.profile.permissions.values_list('url_pattern', flat=True),
                request.user.usergroup_set.values_list('permissions__url_pattern', flat=True)
            )
        ):
            if re.match(url_pattern, url):
                return SuccessfulResponse()
        return ForbiddenResponse()


class DumpView(views.APIView):
    def get(self, request):
        return SuccessfulResponse()
