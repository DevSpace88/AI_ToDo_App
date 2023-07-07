import json

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse

from utils.db_query import answer_query

from .models import Task, Todo


def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'todo/tasks.html', {'tasks': tasks})

def todos(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    todos = task.steps.all()
    
    return render(request, 'todo/todos.html', {'task': task, 'todos': todos})

# normal create_task-function
def create_task(request):
    name = request.POST.get('task', '')
    task = Task.objects.create(name=name)
    todos = task.steps.all()
    
    return redirect(reverse('todos', kwargs={'task_id': task.id}))

def create_ai_task(request):
    if request.method == 'POST':
        query = request.POST.get('task', '')
        
        if len(query) > 100:
            return redirect('tasks')
        
        context = """
            I need a step-by-step guide along with the corresponding code to solve the task. The answer should be a doable step to code something. Divide answer into small coding steps with a title and a description. print the answer in a json datastructure, that looks like the example below. If there are several points in one description just divide it further into smaller todos with steps, but only if it is necessary. In the json, summarize what the user asked in a short sentence that sounds like a todo-task and print it as value for the "name"-key. The titles should never have the character of a question, but of a todo list todo title. Never print anything, that only refers the user to go to the django documentation. You can refer to the specfic documentation of the current step as a link as the last point in the description. Please orient yourself on the example json below, dont forget that every todo has a order that is basically the current step number that also should be printed in the datastructure. Print nothing else besides this JSON-Datastructure. If an error occures, still print the same data structure but with error in title and error in description. Dont user square brackets only curved brackets! It should look like the following example:
        
            {
                "task": {
                    "name": "Task Name",
                    "steps": [
                        {
                            "title": "Step 1: Todoname 1",
                            "description": "Provide a detailed description of the first step, explaining what needs to be done to solve the problem.
                            
                            code:

                            // Place the code for the second step here
                            
                            Additional Information:
                            Include any additional information that may be relevant to the problem, such as the programming language you are using or specific constraints that need to be considered.
                            https://docs.djangoproject.com/en/4.2/topics/db/models/",
                            "is_done": False,
                            "order": 1,
                        },
                        {
                            "title": "Step 2: Todoname 2",
                            "description": "Provide a detailed description of the second step, explaining what needs to be done to proceed.
                            
                            code:

                            // Place the code for the second step here
                            
                            Additional Information:
                            Include any additional information that may be relevant to the problem, such as the programming language you are using or specific constraints that need to be considered.
                            source: https://docs.djangoproject.com/en/4.2/topics/db/models/#verbose-field-names,
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
        order= 0
        
        for step in steps:
            title = step['title']
            description = step['description']
            is_done = False
            order += 1
            Todo.objects.create(task=task, title=title, description=description, is_done=is_done, order=order)

        return redirect(reverse('todos', kwargs={'task_id': task.id}))

     
def edit_todo(request, task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        todo.title = request.POST.get('title', '')
        
        if todo.title.strip():  # Check if the updated title is not empty after stripping whitespace
            todo.save()

        return render(request, 'todo/partials/todo.html', {'task': task, 'todo': todo})
    
    return render(request, 'todo/partials/edit-todo.html', {'task': task, 'todo': todo})


def edit_description(request,task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        todo.description = request.POST.get("description", "")
        
        if todo.description.strip():  # Check if the updated description is not empty after stripping whitespace
            todo.save()

        return render(request, 'todo/partials/todo.html', {'task': task, 'todo': todo})
    
    return render(request, 'todo/partials/edit-description.html', {'task': task, 'todo': todo})

def add_todo(request, task_id):
    todo = None
    task = get_object_or_404(Task, id=task_id)
    title = request.POST.get('title', '')

    if title:
        todo = Todo.objects.create(task=task, title=title)
    
    return render(request, 'todo/partials/todo.html', {'task': task, 'todo': todo})

def update_todo(request, task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)
    todo.is_done = True
    todo.save()

    return render(request, 'todo/partials/todo.html', {'task': task, 'todo': todo})

def delete_todo(request, task_id, pk):
    task = get_object_or_404(Task, id=task_id)
    todo = Todo.objects.get(pk=pk)
    todo.delete()

    return HttpResponse()

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('tasks')