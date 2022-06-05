from django.shortcuts import render
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    todos = Todo.objects.all()
    completed_count = todos.filter(is_completed=True).count()
    incomplete_count = todos.filter(is_completed=False).count()
    all_count = todos.count()
    context = {'todos': show_todos(request, todos), 'completed_count': completed_count, 'incomplete_count': incomplete_count, 'all_count': all_count}
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
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    return render(request, 'todo/todo-details.html', context)


def show_todos(request, todos):
    if request.GET.get("filter")=='incomplete':
        return todos.filter(is_completed=False)
    elif request.GET.get("filter")=='complete':
        return todos.filter(is_completed=True)
    else:
        return todos.all()

