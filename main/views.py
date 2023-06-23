from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django import forms

from .forms import TaskForm, StepForm
from .models import Step, Task

# Create your views here.

class IndexView(TemplateView):
    template_name = "main/index.html"

class TaskList(ListView):
    model = Task
    template_name = "main/tasks.html"
    context_object_name = "tasks"

# class StepList(ListView):
#     model = Step
#     template_name = "step.html"
#     context_object_name = "steps"


    
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    steps = task.steps.order_by('order')
    return render(request, 'main/task_detail.html', {'task': task, 'steps': steps})


def create_task(request):
    StepFormSet = forms.formset_factory(StepForm, extra=1)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        formset = StepFormSet(request.POST, prefix='step')

        if form.is_valid() and formset.is_valid():
            task_name = form.cleaned_data['task_name']
            task = Task.objects.create(name=task_name)

            for step_form in formset:
                step_name = step_form.cleaned_data['name']
                Step.objects.create(task=task, name=step_name, order=step_form.prefix)

            return redirect('task_list')
    else:
        form = TaskForm()
        formset = StepFormSet(prefix='step')

    return render(request, 'main/create_task.html', {'form': form, 'formset': formset})


