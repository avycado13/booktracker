from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import List


@receiver(post_save, sender=User)
def create_default_lists(sender, instance, created, **kwargs):
    if created:
        List.objects.create(user=instance, name="To Be Read")
        List.objects.create(user=instance, name="Read Books")
