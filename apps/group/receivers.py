from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction

from .models import User, Profile


def create_profile(user):
    """
    Create Profile if required when user is saved
    """
    profile = Profile.objects.filter(user_id=user.id).first()
    if profile:
        profile.save()
    return Profile.objects.create(user=user)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """
    Signal to auto create or save user profile instance whenever
    the user is saved.
    """
    if created or Profile.objects.filter(user=instance).count() == 0:
        """
        on_commit is used because ultimately Profile is created with m2m permissions field
        which require user's id
        """
        transaction.on_commit(lambda: create_profile(instance))
    else:
        instance.profile.save()
