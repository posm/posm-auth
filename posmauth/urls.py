from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.contrib.auth import views as auth_views

from group.views import (
    PermissionValidationView,
    AssignedPermissionListView,
    LoginView,
    Error400,
    DummyView,
)

urlpatterns = [
    path('', RedirectView.as_view(url='login')),

    path('admin/', admin.site.urls),

    path('permission-validate/', PermissionValidationView.as_view()),
    path('assigned-permissions/', AssignedPermissionListView.as_view()),
    re_path(r'(403|404)/', Error400.as_view()),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='posm/change_password.html',
        success_url='login',
    ), name='password_change'),
]

if settings.DEBUG:
    urlpatterns.append(re_path('(dump/|dump)', DummyView.as_view()))
