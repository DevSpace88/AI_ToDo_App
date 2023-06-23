from django import forms

class TaskForm(forms.Form):
    task_name = forms.CharField(label='Task')
    # step_names = forms.CharField(label='Step', widget=forms.Textarea)
    step_order = forms.IntegerField(label="order")

class StepForm(forms.Form):
    name = forms.CharField(label='Step Name')
    
    #noch eine create-tep seite vermutlich anlegen