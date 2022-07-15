from django.shortcuts import render, redirect
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    todos = Todo.objects.filter(owner=request.user)
    completed_count = todos.filter(is_completed=True).count()
    incomplete_count = todos.filter(is_completed=False).count()
    all_count = todos.count()
    context = {'todos': show_todos(request, todos), 'completed_count': completed_count, 'incomplete_count': incomplete_count, 'all_count': all_count}
    return render(request, 'todo/index.html', context)


@login_required
def create_todo(request):
    if request.method == "POST":
        todo = Todo()
        todo.title = request.POST.get("title")
        todo.description = request.POST.get("description")
        todo.is_completed = True if request.POST.get("is_completed", False) == 'on' else False
        todo.owner = request.user
        todo.save()
        messages.add_message(request, messages.SUCCESS, "Todo Created Successfully")
        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))
    form = TodoForm()
    context = {'form': form}
    return render(request, 'todo/create_todo.html', context)


@login_required
def todo_details(request, id):
    todo = get_object_or_404(Todo, pk=id)
    if todo.owner == request.user:
        context = {'todo': todo}
        return render(request, 'todo/todo-details.html', context)
    else:
        messages.add_message(request, messages.ERROR, "You do no have access for this operation")
        return redirect(reverse('home'))


@login_required
def show_todos(request, todos):
    if request.GET.get("filter") == 'incomplete':
        return todos.filter(is_completed=False)
    elif request.GET.get("filter") == 'complete':
        return todos.filter(is_completed=True)
    else:
        return todos.all()


@login_required
def todo_delete(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    if todo.owner == request.user:
        if request.method == "POST":
            todo.delete()
            messages.add_message(request, messages.ERROR, "Todo Deleted Successfully")
            return HttpResponseRedirect(reverse('home'))
        return render(request, 'todo/todo-delete.html', context)
    else:
        messages.add_message(request, messages.ERROR, "You do no have access for this operation")
        return redirect(reverse('home'))


@login_required
def edit_todo(request, id):
    todo = get_object_or_404(Todo, pk=id)
    if todo.owner == request.user:
        form = TodoForm(instance=todo)
        context = {'form': form, 'todo': todo}
        if request.method == "POST":
            todo.title = request.POST.get("title")
            todo.description = request.POST.get("description")
            todo.is_completed = True if request.POST.get("is_completed", False) == 'on' else False
            todo.save()
            messages.add_message(request, messages.SUCCESS, "Todo Updated Successfully")
            return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))
        return render(request, 'todo/edit-todo.html', context)
    else:
        messages.add_message(request, messages.ERROR, "You do no have access for this operation")
        return redirect(reverse('home'))