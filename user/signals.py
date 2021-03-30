from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def makeProfile(sender, instance, created, **kwargs):
    print('make profile')
    if created:
        print('save profile')
        Profile(user=instance).save()
