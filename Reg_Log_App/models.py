from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Create an authentication token for a user upon user creation.
    Parameters:
    - sender: The sender model (settings.AUTH_USER_MODEL).
    - instance: The user instance being created.
    - created: A boolean indicating if the user instance is being created.
    """
    if created:
        Token.objects.create(user=instance)
        