from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField(auto_created=False, auto_now=False)
    timeleft = models.IntegerField(null=True, blank=True, default=None)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.title} - ({self.owner})"