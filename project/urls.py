from django.urls import path

from . import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="index"),
    path("logout/", views.logout_page, name="logout"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path('add/', views.TaskAddView.as_view(), name='add'),
    path('update<str:pk>/', views.TaskUpdateView.as_view(), name='update'),
    path('task/<str:pk>/', views.TaskDetailView.as_view(), name='detail'),
    path('delete/<str:pk>/', views.TaskDeleteView.as_view(), name='delete'),
]
