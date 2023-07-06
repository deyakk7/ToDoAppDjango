from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField(null=True, blank=True, auto_created=False, auto_now=False, default=None)
    timeleft = models.IntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.title} - ({self.owner})"