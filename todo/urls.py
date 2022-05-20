from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name="home"),
    path('create_todo', views.create_todo, name="create-todo"),
    path('todo/<id>', views.todo_details, name="todo")
]