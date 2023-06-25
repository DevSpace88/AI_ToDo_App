from django.contrib import admin
from .models import Todo, Task

# Register your models here.
admin.site.register(Task)
admin.site.register(Todo)