from django.urls import path

from todo.views import (add_todo, create_ai_task, create_task, delete_task,
                        delete_todo, edit_description, edit_todo, tasks, todos,
                        update_todo)

urlpatterns = [
    path('', tasks, name='tasks'),
   
    path('tasks/<int:task_id>/', todos, name='todos'),
    path('tasks/<int:task_id>/add-todo/', add_todo, name='add_todo'),
    path('tasks/<int:task_id>/edit-todo/<int:pk>/', edit_todo, name='edit_todo'),
    path('tasks/<int:task_id>/edit-description/<int:pk>/', edit_description, name='edit_description'),
    path('tasks/<int:task_id>/update/<int:pk>/', update_todo, name='update_todo'),
    path('tasks/<int:task_id>/delete/<int:pk>/', delete_todo, name='delete_todo'),
    
    path('tasks/create-task/', create_task, name='create_task'),
    path('tasks/create-ai-task/', create_ai_task, name='create_ai_task'),
    path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),
]
