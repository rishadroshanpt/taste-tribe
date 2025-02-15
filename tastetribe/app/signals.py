from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.contrib.auth.models import User

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:  # Only create notification when a new follow is created
        # Notify the user being followed
        Notification.objects.create(
            user=instance.following,
            message="started following you",
        )

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:  # Only create notification when a new like is added
        # Notify the user who posted the liked post
        Notification.objects.create(
            user=instance.dish.user,
            message="liked your post",
        )

@receiver(post_save, sender=User)
def create_user_bio(sender, instance, created, **kwargs):
    # Automatically create a Bio when a new User is created
    if created:
        Bio.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_bio(sender, instance, **kwargs):
    # Save the user's bio if it is updated
    instance.bio.save()