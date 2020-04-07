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

    def save(self, *args, **kwargs):
        """
        NOTE: Conflicts occur between the User's post_save receiver and admin panel's
        user save action. This occurs because admin panel's action automatically creates
        profile without the use of signals, And whenever user is created, our receiver
        tries to create profile with the same user.
        Check this by overriding this save method which checks for duplicate entries
        """
        if not self.id and Profile.objects.filter(user_id=self.user.id).first():
            return Profile.objects.get(user_id=self.user.id)
        return super().save(*args, **kwargs)

    def get_allowed_posm_components(self):
        return PosmComponentPermission.objects.filter(
            Q(usergroup__members=self.user) | Q(profile__user=self.user)
        ).distinct()

    def get_display_name(self):
        return self.user.get_full_name() if self.user.first_name \
            else self.user.username
