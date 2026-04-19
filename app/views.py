from django.shortcuts import render,redirect
from .models import Task
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import date

# Create your views here.

def task_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')

        Task.objects.create(
            title=title,
            due_date=due_date,
            user=request.user
        )

    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo/task_list.html', {'tasks': tasks})


def update_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.due_date = request.POST.get('due_date')
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('task_list')

    return render(request, 'todo/edit_task.html', {'task': task})


def delete_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.delete()
    return redirect('task_list')

# SIGNUP
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('task_list')
    return render(request, 'todo/signup.html')


# LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('task_list')

    return render(request, 'todo/login.html')


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')

