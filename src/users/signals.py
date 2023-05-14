from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, UserProfile


@receiver(post_save, sender=User)
def update_user_profile_signal(sender: Any, instance: User, created: bool, **kwargs: dict[str, Any]) -> None:
    """Create or update UserProfile model after each user gets created."""
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
