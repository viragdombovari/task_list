from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    #priority = forms.IntegerField(label="Priority", min_value=1, max_value=50)


# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "task/add.html", {
                "form": form
            })   
    return render( request, "tasks/add.html", {
        "form": NewTaskForm()
    })

def delete(request, task_id):
    if "tasks" in request.session:
        tasks = request.session["tasks"]
        if 0 <= task_id < len(tasks):
            tasks.pop(task_id)  
            request.session["tasks"] = tasks  

    return HttpResponseRedirect(reverse("tasks:index"))