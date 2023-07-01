from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        tasks = user.task_set.all()
        if not tasks:
            context['empty'] = True
        else:
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
            return render(request, 'project/index.html', context)
    else:
        pass
    context['form'] = form
        # context['form'] = form
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

