from rest_framework import serializers

from project.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ('timeleft', )
        depth = 1
