from django.shortcuts import render
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def index(request):
    todo = Todo.objects.all()
    context = {'todos': todo}
    return render(request, 'todo/index.html', context)


def create_todo(request):
    if request.method == "POST":
        todo = Todo()
        todo.title = request.POST.get("title")
        todo.description = request.POST.get("description")
        todo.is_completed = True if request.POST.get("is_completed", False) == 'on' else False
        todo.save()
        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))
    form = TodoForm()
    context = {'form': form}
    return render(request, 'todo/create_todo.html', context)


def todo_details(request, id):

    return render(request, 'todo/todo-details.html', {})
