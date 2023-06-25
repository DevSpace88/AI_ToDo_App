from django.contrib import admin
from django.urls import path

from todo.views import tasks, todos, add_todo, update_todo, delete_todo, edit_todo, edit_description

urlpatterns = [
    # path('tasks/', tasks, name='tasks'),
    path('', tasks, name='tasks'),
    path('tasks/<int:task_id>/', todos, name='todos'),
    path('tasks/<int:task_id>/add-todo/', add_todo, name='add_todo'),
    path('tasks/<int:task_id>/update/<int:pk>/', update_todo, name='update_todo'),
    path('tasks/<int:task_id>/delete/<int:pk>/', delete_todo, name='delete_todo'),
    path('tasks/<int:task_id>/edit-todo/<int:pk>/', edit_todo, name='edit_todo'),
    path('tasks/<int:task_id>/edit-description/<int:pk>/', edit_description, name='edit_description'),
    path('admin/', admin.site.urls),
]
