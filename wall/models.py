from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Post(models.Model):
    body = models.TextField("Body", null=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    createdAt = models.DateTimeField("Created At", auto_now_add=True)

    def clean(self):
        if not self.body:
            raise ValidationError('Empty error message')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.body + " By: " + self.author.username
