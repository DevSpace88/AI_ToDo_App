from django.contrib import admin
from django.urls import path

from todo.views import todos, add_todo, update_todo, delete_todo, edit_todo, edit_description

urlpatterns = [
    path('', todos, name='todos'),
    path('add-todo/', add_todo, name='add_todo'),
    path('update/<int:pk>/', update_todo, name='update_todo'),
    path('delete/<int:pk>/', delete_todo, name='delete_todo'),
    path('edit-todo/<int:pk>/', edit_todo, name='edit_todo'),
    path('edit-description/<int:pk>/', edit_description, name='edit_description'),
    path('admin/', admin.site.urls),
]
