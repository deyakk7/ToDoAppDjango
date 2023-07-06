from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from datetime import timedelta, datetime

from . import forms
from .models import Task

# Create your views here.


def index(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        tasks = user.task_set.all().order_by('complete', 'due')
        if not tasks:
            context['empty'] = True
        else:
            for task in tasks:
                timeleft = task.due - datetime.now(timezone.utc)
                timeleft = max(0, int(timeleft.total_seconds()))
                task.timeleft = timeleft
            context['tasks'] = tasks
    return render(request, 'project/index.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('index')

    context = {}
    form = forms.CustomUserCreationForm()
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
    else:
        pass
    context['form'] = form
    return render(request, 'project/register.html', context)


def login_page(request):
    context = {}
    form = forms.CustomUserLogin()
    context['form'] = form
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = forms.CustomUserLogin(request.POST)
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        context['form'] = form
        if user is not None:
            login(request, user)
            return redirect('index')

        else:
            context['error'] = 'Username or password is incorrect'
    return render(request, 'project/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def add(request):
    form = forms.TaskForm()
    if request.method == 'POST':
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            current_task = form.save(commit=False)
            current_task.owner = request.user
            current_task.save()
            return redirect('index')
    return render(request, 'project/add.html', {'form': form})


def update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner != request.user:
        return redirect('index')
    form = forms.TaskForm(instance=task)
    if request.method == 'POST':
        form = forms.TaskForm(request.POST, instance=task)
        if form.is_valid():
            current_task = form.save(commit=False)
            current_task.save()
            return redirect('index')
    return render(request, 'project/update.html', {'form': form})


def detail(requets, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner != requets.user:
        return redirect('index')
    timeleft = task.due - datetime.now(timezone.utc)
    timeleft = max(0, int(timeleft.total_seconds()))
    task.timeleft = timeleft
    return render(requets, 'project/detail.html', {'task': task})


def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner != request.user:
        return redirect('index')
    if request.method == 'POST':
        task.delete()
        return redirect('index')
    return render(request, 'project/delete.html', {'task': task})
