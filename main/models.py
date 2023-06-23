from django.db import models

# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=100)
    # brauchen bestimmt beide ne id
    
    def __str__(self):
        return self.name
    
class Step(models.Model):
    task = models.ForeignKey(Task, related_name='steps', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField() #ändern in positiveinteger
    

    class Meta:
        unique_together = ['task', 'order']
        
    
    def __str__(self):
        return self.name