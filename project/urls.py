from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path('add/', views.add, name='add'),
    path('update<str:pk>/', views.update, name='update'),
    path('task/<str:pk>/', views.detail, name='detail'),
    path('delete/<str:pk>/', views.delete, name='delete'),
]
