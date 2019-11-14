from django.contrib.auth.models import User
from django.db.models import Q
from django.db import models


class PosmComponentPermission(models.Model):
    """
    POSM Auth user group model
    """
    code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} (NGINX: {self.code})'


class UserGroup(models.Model):
    """
    POSM Auth user group model
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(PosmComponentPermission)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.title


class Profile(models.Model):
    """
    POSM Auth user group model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(PosmComponentPermission)

    def __str__(self):
        return f'{self.user} Profile'

    def get_allowed_posm_components(self):
        return PosmComponentPermission.objects.filter(
            Q(usergroup__members=self.user) | Q(profile__user=self.user)
        ).distinct()

    def get_display_name(self):
        return self.user.get_full_name() if self.user.first_name \
            else self.user.username
