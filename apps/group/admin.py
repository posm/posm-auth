from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin

from utils.common import camelcase_to_titlecase

from .models import UserGroup, User, Profile


def gen_auth_proxy_model(ModelClass, _label=None):
    label = _label or ModelClass.__name__
    t_label = camelcase_to_titlecase(label)

    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = f'{t_label}'
        verbose_name_plural = f'{t_label}s'
    model = type(f"{label.replace(' ', '_')}", (ModelClass,), {
        '__module__': __name__,
        'Meta': Meta,
    })
    return model


admin.site.unregister(User)
admin.site.unregister(Group)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    filter_horizontal = ('permissions',)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    search_fields = (
        'username', 'first_name', 'last_name', 'email',
    )
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
    )
    fieldsets = (
        (None, {
            'fields': (
                'username', 'email',
                'first_name', 'last_name',
                'password',
                'last_login', 'date_joined',
                'is_staff', 'is_superuser',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


class UserGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions', 'members',)


admin.site.register(gen_auth_proxy_model(UserGroup), UserGroupAdmin)
