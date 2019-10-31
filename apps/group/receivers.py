from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User, Profile


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """
    Signal to auto create or save user profile instance whenever
    the user is saved.
    """
    if created or Profile.objects.filter(user=instance).count() == 0:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
