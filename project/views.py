from typing import Any, Dict
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from datetime import datetime

from . import forms
from .mixins import CustomUserPassesTestMixin, NotLoggedMixin
from .models import Task
from .utils import search_query, paginateTask

"""
CLASS BASED VIEW

"""

class TaskListView(ListView):
    model = Task
    template_name = 'project/index.html'
    context_object_name = 'tasks'
    ordering = ['complete', 'due']
    paginate_by = 1

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        custom_range = context['paginator'].get_elided_page_range(
            context['page_obj'].number, on_each_side=2, on_ends=1)
        context['custom_range'] = custom_range
        sq = self.request.GET.get('search_query')
        if sq:
            context['search_query'] = sq

        return context

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.user.is_authenticated:
            q = self.request.GET.get('search_query')
            if q:
                tasks = self.model.objects.filter(owner=self.request.user, title__icontains=q).order_by('complete', 'due')
            else:
                tasks = self.model.objects.filter(owner=self.request.user).order_by('complete', 'due')
            for task in tasks:
                timeleft = task.due - datetime.now(timezone.utc)
                timeleft = max(0, int(timeleft.total_seconds()))
                task.timeleft = timeleft
            return tasks
        return super().get_queryset()

class UserRegisterView(CreateView):
    template_name = 'project/register.html'
    model = User
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        messages.error(self.request, 'Something goes wrong!')
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        messages.success(self.request, 'User has been created successfully!')
        return super().get_success_url()


class UserLoginView(LoginView):
    template_name = 'project/login.html'
    success_url = reverse_lazy('index')
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        messages.success(
            self.request, f'Welcome, {form.cleaned_data["username"]}!')
        return super().form_valid(form)


#AND LOGOUT FUNCTION :D
def logout_page(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('index')


class TaskAddView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'project/add.html'
    form_class = forms.TaskForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        messages.success(self.request, 'Task added successfully')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Something goes wrong..')
        return self.render_to_response(self.get_context_data(form=form))


class TaskUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'project/update.html'
    form_class = forms.TaskForm

    def form_valid(self, form):
        messages.success(self.request, 'Updated successfully')
        return super().form_valid(form)


class TaskDetailView(CustomUserPassesTestMixin, DetailView):
    template_name = 'project/detail.html'
    context_object_name = 'task'
    model = Task
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timeleft = self.get_object().due - datetime.now(timezone.utc)
        timeleft = max(0, int(timeleft.total_seconds()))
        context['timeleft'] = timeleft
        return context


class TaskDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'project/delete.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')

    def get_success_url(self) -> str:
        messages.success(self.request, 'deleted successfully')
        return super().get_success_url()


"""
FUNCTION BASED VIEWS

"""

def index(request):
    context = {}
    if request.user.is_authenticated:
        tasks, search, empty = search_query(request)
        custom_range, tasks = paginateTask(request, tasks, 3)
        context['custom_range'] = custom_range
        context['tasks'] = tasks
        if search:
            context['search_query'] = search
        context['empty'] = empty
        

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
    print(type(task.timeleft))
    return render(requets, 'project/detail.html', {'task': task})


def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner != request.user:
        return redirect('index')
    if request.method == 'POST':
        task.delete()
        return redirect('index')
    return render(request, 'project/delete.html', {'task': task})
