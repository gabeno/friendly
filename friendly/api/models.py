import unicodedata

import bcrypt
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=50, unique=True)
    content = models.CharField(max_length=300, default="Add content ...")
    created_when = models.DateTimeField(default=timezone.now)
    likes_count = models.IntegerField(default=0)
    author_id = models.IntegerField(default=99)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    created_when = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=63)
    geo_data = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        super().full_clean(exclude=["geo_data"])
        super().save(*args, **kwargs)

    def hash_password(raw_password):
        return str(
            bcrypt.hashpw(
                unicodedata.normalize("NFKC", raw_password).encode("utf8"),
                bcrypt.gensalt(),
            ),
            "utf8",
        )

    def check_password(self, raw_password):
        return bcrypt.checkpw(
            unicodedata.normalize("NFKC", raw_password).encode("utf8"),
            bytes(self.password, "utf8"),
        )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"
