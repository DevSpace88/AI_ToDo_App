from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Task, Todo

def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'todo/tasks.html', {'tasks': tasks})


def todos(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    todos = task.steps.all()

    return render(request, 'todo/todos.html', {'task': task, 'todos': todos})


@require_http_methods(['GET', 'POST'])
def edit_todo(request, pk):
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        todo.title = request.POST.get('title', '')
        todo.save()

        return render(request, 'todo/partials/todo.html', {'todo': todo})
    
    return render(request, 'todo/partials/edit-todo.html', {'todo': todo})

def edit_description(request,task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        todo.description = request.POST.get("description", "")
        todo.save()

        return render(request, 'todo/partials/todo.html', {'todo': todo})
    
    return render(request, 'todo/partials/edit-description.html', {'task': task, 'todo': todo})

@require_http_methods(['POST'])
def add_todo(request, task_id):
    # todo = None
    task = get_object_or_404(Task, id=task_id)
    title = request.POST.get('title', '')

    if title:
        todo = Todo.objects.create(task=task_id, title=title)
    
    return render(request, 'todo/partials/todo.html', {'task': task, 'todo': todo})

@require_http_methods(['PUT'])
def update_todo(request, task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)
    todo.is_done = True
    todo.save()

    return render(request, 'todo/partials/todo.html', {'todo': todo})

@require_http_methods(['DELETE'])
def delete_todo(request, task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)
    todo.delete()

    return HttpResponse()