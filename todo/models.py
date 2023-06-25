from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f'{self.title} {self.description} {self.is_done}'