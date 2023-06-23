from .views import TaskList, IndexView, task_detail, create_task

from django.urls import path

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tasks/', TaskList.as_view(), name="tasks"),
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),
    path('create-task', create_task, name="create-task")
    
]