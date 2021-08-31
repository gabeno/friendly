import unicodedata

import bcrypt
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    created_when = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=100)
    geo_data = models.JSONField(default=dict)
    created_on_holiday = models.JSONField(default=dict)

    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super().full_clean(exclude=["geo_data", "created_on_holiday"])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class Post(models.Model):
    content = models.CharField(max_length=300)
    created_when = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name="likes")
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="posts"
    )

    def save(self, *args, **kwargs):
        super().full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"
