from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Task(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name}'


class Todo(models.Model):
    task = models.ForeignKey(Task, related_name='steps', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    order = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ['task', 'order']
    
    def __str__(self):
        return f'{self.title} {self.description} {self.is_done} {self.task}'

@receiver(pre_save, sender=Todo)
def set_todo_order(sender, instance, **kwargs):
    if instance.order is None:
        # Find the maximum order value for the given task
        max_order = Todo.objects.filter(task=instance.task).aggregate(models.Max('order'))['order__max']
        instance.order = max_order + 1 if max_order is not None else 1