from rest_framework import generics, viewsets, mixins
from .permissions import DeyakkPermision

from .serializers import *
from project.models import Task
from django.contrib.auth.models import User

class TaskViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet
):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [DeyakkPermision]


