from django.contrib.auth.models import User
from django.db import models


class PosmComponentPermission(models.Model):
    """
    POSM Auth user group model
    """
    code = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return f'{self.code}'


class UserGroup(models.Model):
    """
    POSM Auth user group model
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
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
