from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404,  reverse
from django.views.decorators.http import require_http_methods

from utils.db_query import answer_query


from .models import Task, Todo

# import json
from django.http import JsonResponse



def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'todo/tasks.html', {'tasks': tasks})


def todos(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    todos = task.steps.all()
    
    return render(request, 'todo/todos.html', {'task': task, 'todos': todos})


def create_task(request):
    name = request.POST.get('task', '')
    task = Task.objects.create(name=name)

    if request.method == 'POST':
        query = request.POST.get('query', '')
        context = """
            Never print anything, that refers the user to go to the django documentation. The answer should be a doable step to code something. Divide answer into small coding steps with a title and a description. print the answer in a json datastructure, where a field called todo, has numbered fields for title and numbered fields for description accordingly, to a specific task field. If there are several points in one description you can use - as a bullet point, but only if it is necessary. In a json-field, calles "task-title", that is in the same nesting as "todo", but comes before, summarize what the user asked in short sentence that sounds like a todo-task. Print nothing else besides a this JSON-Datastructure. If an error is created print the same data structure but with error in title and error in description. The titles should never have the character of a question, but of a todo list todo title. It should look like this example: {
        
                {
                    "task": {
                        "task-title": "Setting up Django models",
                        "todo": {
                            "1": {
                                "title": "Create a Django model",
                                "description": "- Open your Django project and locate the directory that contains your app. This is usually the directory that has a manage.py file.\n\n- Inside your app directory, open the file models.py. This is where you define your models.\n\n- Import the necessary modules from Django, such as models. You can add the import statement at the top of the models.py file."
                            },
                            "2": {
                                "title": "Add the import statement at the top of the models.py file.",
                                "description": "- from django.db import models"
                            },
                            "3": {
                                "title": "Define your model as a subclass of models.Model. Each attribute of the model represents a field in the database table.",
                                "description": "- class YourModel(models.Model):\n    field1 = models.CharField(max_length=100)\n    field2 = models.IntegerField()\n    field3 = models.DateTimeField()\n\n- Customize the fields according to your needs. Django provides various field types, such as CharField for strings, IntegerField for integers, DateTimeField for date and time values, and many more. You can specify additional parameters like max_length, default, null, blank, etc., based on your requirements.\n\n- Optionally, define any relationships between models using fields like ForeignKey, OneToOneField, or ManyToManyField. This allows you to establish relationships between different models."
                            }
                        }
                    }
                }
        """
    
        data = answer_query(query, context)

        task_data = data.get('task', {})
        task_title = task_data.get('task-title', '')
        
        if task_title:
            task_object = Task.objects.create(name=task_title)

            todo_data = task_data.get('todo', {})
            for todo_key, todo_info in todo_data.items():
                title = todo_info.get('title', '')
                description = todo_info.get('description', '')

                Todo.objects.create(
                    task=task_object,
                    title=title,
                    description=description
                )

        return redirect(reverse('todos', kwargs={'task_id': task_object.id, 'data': data}))

    return redirect(reverse('todos', kwargs={'task_id': task_object.id}))

    
# def create_task(request):
#     name = request.POST.get('task', '')
   
    
#     if request.method == 'POST':
#         query = request.POST.get('query', '')
    
   
    
#         context = """
#             Never print anything, that refers the user to go to the django documentation. The answer should be a doable step to code something. Divide answer into small coding steps with a title and a description. print the answer in a json datastructure, where a field called todo, has numbered fields for title and numbered fields for description accordingly, to a specific task field. If there are several points in one description you can use - as a bullet point, but only if it is necessary. In a json-field, calles "task-title", that is in the same nesting as "todo", but comes before, summarize what the user asked in short sentence that sounds like a todo-task. Print nothing else besides a this JSON-Datastructure. If an error is created print the same data structure but with error in title and error in description. The titles should never have the character of a question, but of a todo list todo title. It should look like this example: {
        
#                 {
#                     "task": {
#                         "task-title": "Setting up Django models",
#                         "todo": {
#                             "1": {
#                                 "title": "Create a Django model",
#                                 "description": "- Open your Django project and locate the directory that contains your app. This is usually the directory that has a manage.py file.\n\n- Inside your app directory, open the file models.py. This is where you define your models.\n\n- Import the necessary modules from Django, such as models. You can add the import statement at the top of the models.py file."
#                             },
#                             "2": {
#                                 "title": "Add the import statement at the top of the models.py file.",
#                                 "description": "- from django.db import models"
#                             },
#                             "3": {
#                                 "title": "Define your model as a subclass of models.Model. Each attribute of the model represents a field in the database table.",
#                                 "description": "- class YourModel(models.Model):\n    field1 = models.CharField(max_length=100)\n    field2 = models.IntegerField()\n    field3 = models.DateTimeField()\n\n- Customize the fields according to your needs. Django provides various field types, such as CharField for strings, IntegerField for integers, DateTimeField for date and time values, and many more. You can specify additional parameters like max_length, default, null, blank, etc., based on your requirements.\n\n- Optionally, define any relationships between models using fields like ForeignKey, OneToOneField, or ManyToManyField. This allows you to establish relationships between different models."
#                             }
#                         }
#                     }
#                 }
        
#                     """

    
#         data = answer_query(query, context)

#         task_data = data.get('task', {})
#         task_title = task_data.get('task-title', '')
        
#         if task_title:
#             task_object = Task.objects.create(name=task_title)

#             todo_data = task_data.get('todo', {})
#             for todo_key, todo_info in todo_data.items():
#                 title = todo_info.get('title', '')
#                 description = todo_info.get('description', '')

#                 Todo.objects.create(
#                     task=task_object,
#                     title=title,
#                     description=description
#                 )

#             # Retrieve the updated todos for the task
#             todos = task_object.steps.all()
#             todos.save()
        

    
#         return redirect(reverse('todos', kwargs={'task_id': task_object.id}) + f'?data={data}')

#     return JsonResponse(data)

# normale create_task-funktion
# def create_task(request):
#     name = request.POST.get('task', '')
#     task = Task.objects.create(name=name)
#     todos = task.steps.all()
    
#     return redirect(reverse('todos', kwargs={'task_id': task.id}))



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