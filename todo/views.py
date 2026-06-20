from django.shortcuts import get_object_or_404, render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required(login_url='login')
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    context = {
        'tasks': tasks,
        'search_query': search_query,
    }
    return render(request, 'todo/index.html', context)


@login_required(login_url='login')
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            task = Task(title=title, user=request.user)
            task.save()
    return redirect('tasks-list')


@login_required(login_url='login')
def task_update(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.complete = request.POST.get('complete') == 'on'
        task.save()
        return redirect('tasks-list')
    context = {'task': task}
    return render(request, 'todo/update_task.html', context)


@login_required(login_url='login')
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect('tasks-list')
 