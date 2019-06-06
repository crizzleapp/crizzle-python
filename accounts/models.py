from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from guardian.mixins import GuardianUserMixin


class User(GuardianUserMixin, AbstractUser):
    pass


def get_anonymous_user_instance(user_model) -> User:
    """
    Used by Django-guardian during migrations.
    Should return a User instance
    """
    return user_model(username=settings.ANONYMOUS_USER_NAME, )
