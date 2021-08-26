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
