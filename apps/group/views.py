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
        module = request.headers['X-POSM-AUTH-MODULE']
        if (
                request.user.profile.permissions.filter(code=module).exists() or
                request.user.usergroup_set.filter(permissions__code=module).exists()
        ):
            return SuccessfulResponse()
        return ForbiddenResponse()


class DummyView(views.APIView):
    """
    Just a dummy response view
    """
    def get(self, request):
        return SuccessfulResponse()
