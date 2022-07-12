from utils.setup_test import TestSetup
from django.contrib.messages import get_messages
from django.urls import reverse
from todo.models import Todo


class TestViews(TestSetup):

    def test_should_not_show_create_todo_without_login(self):
        response = self.client.get(reverse('create-todo'))
        self.assertEqual(response.status_code, 302)

    def test_should_create_todo_with_login(self):
        user = self.register_user()
        self.client.post(reverse('register'), user)
        activated_user = self.activate_user(user['username'])
        self.client.login(username=user['username'], password=user['password'])
        todo = self.create_todo()
        todo_initial = Todo.objects.all().count()
        response = self.client.post(reverse('create-todo'), {
            'title': todo['title'],
            'description': todo['description'],
            'user': activated_user
        })
        self.assertEqual(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        self.assertIn("Todo Created Successfully", list(map(lambda x: x.message, storage)))
        todo_later = Todo.objects.all().count()
        self.assertEqual(todo_later, todo_initial+1)