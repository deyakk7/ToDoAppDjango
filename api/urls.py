from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    # path('tasks/', views.TaskListAPIView.as_view()),
    # path('task/<str:pk>/', views.TaskReadUpdateDeleteView.as_view()),
    path('', include(router.urls)),
]
