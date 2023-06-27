import json

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_http_methods

from utils.db_query import answer_query

from .models import Task, Todo


def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'todo/tasks.html', {'tasks': tasks})


def todos(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    todos = task.steps.all()
    
    return render(request, 'todo/todos.html', {'task': task, 'todos': todos})


def create_task(request):
    if request.method == 'POST':
        query = request.POST.get('task', '')
        context = """
            Never print anything, that refers the user to go to the django documentation. The answer should be a doable step to code something. Divide answer into small coding steps with a title and a description. print the answer in a json datastructure, that looks like the example below. If there are several points in one description you can use - as a bullet point, but only if it is necessary. In the json, summarize what the user asked in short sentence that sounds like a todo-task and print it as value for the "name"-key. The titles should never have the character of a question, but of a todo list todo title. Print nothing else besides this JSON-Datastructure. If an error occures, print the same data structure but with error in title and error in description.  It should look like this example:
        
            {
                "task": {
                    "name": "Task Name",
                    "steps": [
                        {
                            "title": "Todo 1",
                            "description": "Description 1",
                            "is_done": False,
                            "order": 1,
                        },
                        {
                            "title": "Todo 2",
                            "description": "Description 2",
                            "is_done": False,
                            "order": 2,
                        }
                    ]
                }
            }

        
        """
    
        raw_data = answer_query(query, context)
        print(raw_data)

        answer = raw_data['answer']
        parsed_answer = json.loads(answer)
        task_name = parsed_answer['task']['name']
        steps = parsed_answer['task']['steps']

        task = Task.objects.create(name=task_name)

        for step in steps:
            title = step['title']
            description = step['description']
            is_done = False
            order = step['order']
            Todo.objects.create(task=task, title=title, description=description, is_done=is_done, order=order)

        return redirect(reverse('todos', kwargs={'task_id': task.id}))

     
@require_http_methods(['GET', 'POST'])
def edit_todo(request, task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        todo.title = request.POST.get('title', '')
        
        if todo.title.strip():  # Check if the updated title is not empty after stripping whitespace
            todo.save()

        return render(request, 'todo/partials/todo.html', {'task': task, 'todo': todo})
    
    return render(request, 'todo/partials/edit-todo.html', {'task': task, 'todo': todo})


@require_http_methods(['GET', 'POST'])
def edit_description(request,task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        todo.description = request.POST.get("description", "")
        
        if todo.description.strip():  # Check if the updated title is not empty after stripping whitespace
            todo.save()

        return render(request, 'todo/partials/todo.html', {'task': task, 'todo': todo})
    
    return render(request, 'todo/partials/edit-description.html', {'task': task, 'todo': todo})

@require_http_methods(['POST'])
def add_todo(request, task_id):
    todo = None
    task = get_object_or_404(Task, id=task_id)
    title = request.POST.get('title', '')

    if title:
        todo = Todo.objects.create(task=task, title=title)
    
    return render(request, 'todo/partials/todo.html', {'task': task, 'todo': todo})

@require_http_methods(['PUT'])
def update_todo(request, task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)
    todo.is_done = True
    todo.save()

    return render(request, 'todo/partials/todo.html', {'task': task, 'todo': todo})

@require_http_methods(['DELETE'])
def delete_todo(request, task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)
    todo.delete()

    return HttpResponse()


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('tasks')