from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default='default_avatar.png', upload_to='media-files', null=True, blank=True)