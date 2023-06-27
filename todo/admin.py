from django.contrib import admin
from .models import Todo, Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at',]


class TodoAdmin(admin.ModelAdmin):
    list_display =  ['title', 'task', 'is_done']

admin.site.register(Todo, TodoAdmin)
admin.site.register(Task, TaskAdmin)