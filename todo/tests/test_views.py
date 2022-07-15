from utils.setup_test import TestSetup
from django.contrib.messages import get_messages
from django.urls import reverse
from todo.models import Todo


class TestViews(TestSetup):

    def test_should_not_show_create_todo_without_login(self):
        response = self.client.get(reverse('create-todo'))
        self.assertEqual(response.status_code, 302)

    def test_should_show_create_todo_with_login(self):
        self.login()
        response=self.client.get(reverse('create-todo'))
        self.assertEqual(response.status_code,200)

    def test_should_create_todo_with_login(self):
        activated_user = self.login()
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

    def test_should_show_index_with_login(self):
        self.login()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_should_show_todo_details_with_login(self):
        activated_user = self.login()
        todo = self.create_todo()
        self.client.post(reverse('create-todo'), {
            'title': todo['title'],
            'description': todo['description'],
            'user': activated_user
        })
        response = self.client.get(reverse('todo', kwargs={'id':1}))
        self.assertEqual(response.status_code, 200)

    def test_should_not_show_todo_details_without_login(self):
        todo = self.create_todo()
        self.client.post(reverse('create-todo'), {
            'title': todo['title'],
            'description': todo['description']
        })
        response = self.client.get(reverse('todo', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

    def test_should_not_show_todo_details_with_different_login(self):
        user1 = self.create_test_user(username='pqr', email='pqr@gmail.com', password="password")
        self.login(user1, passwrd="password")
        self.create_todo_with_user(user1)
        user2 = self.create_test_user(username='abc', email='abc@gmail.com', password="password")
        self.login(user2, passwrd="password")
        self.create_todo_with_user(user2)
        response = self.client.get(reverse('todo', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        self.assertIn("You do no have access for this operation", list(map(lambda x: x.message, storage)))

    def test_should_not_show_todo_delete_without_login(self):
        response = self.client.get(reverse('todo-delete', kwargs={'id':1}))
        self.assertEqual(response.status_code, 302)

    def test_should_show_todo_delete_with_login(self):
        user = self.login()
        todo = self.create_todo_with_user(user)
        response = self.client.get(reverse('todo-delete', kwargs={'id': todo.pk}))
        self.assertEqual(response.status_code, 200)

    def test_should_delete_todo_delete_with_login(self):
        user = self.login()
        todo = self.create_todo_with_user(user)
        response = self.client.post(reverse('todo-delete', kwargs={'id': todo.pk}))
        self.assertEqual(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        self.assertIn("Todo Deleted Successfully", list(map(lambda x: x.message, storage)))

    def test_should_not_show_todo_delete_with_different_login(self):
        user1 = self.create_test_user(username='pqr', email='pqr@gmail.com', password="password")
        self.login(user1, passwrd="password")
        self.create_todo_with_user(user1)
        user2 = self.create_test_user(username='abc', email='abc@gmail.com', password="password")
        self.login(user2, passwrd="password")
        self.create_todo_with_user(user2)
        response = self.client.get(reverse('todo-delete', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        self.assertIn("You do no have access for this operation", list(map(lambda x: x.message, storage)))

    def test_should_not_show_edit_todo_without_login(self):
        response = self.client.get(reverse('edit-todo', kwargs={'id':1}))
        self.assertEqual(response.status_code, 302)

    def test_should_show_todo_edit_with_login(self):
        user = self.login()
        todo = self.create_todo_with_user(user)
        response = self.client.get(reverse('edit-todo', kwargs={'id': todo.pk}))
        self.assertEqual(response.status_code, 200)

    def test_should_edit_todo_with_login(self):
        user = self.login()
        todo = self.create_todo_with_user(user)
        todo1=self.create_todo()
        response = self.client.post(reverse('edit-todo', kwargs={'id': todo.pk}),{
            'title':todo1['title'],
            'description': todo1['description'],
        })
        self.assertEqual(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        self.assertIn("Todo Updated Successfully", list(map(lambda x: x.message, storage)))

    def test_should_not_show_edit_todo_with_different_login(self):
        user1 = self.create_test_user(username='pqr', email='pqr@gmail.com', password="password")
        self.login(user1, passwrd="password")
        self.create_todo_with_user(user1)
        user2 = self.create_test_user(username='abc', email='abc@gmail.com', password="password")
        self.login(user2, passwrd="password")
        self.create_todo_with_user(user2)
        response = self.client.get(reverse('edit-todo', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)
        storage = get_messages(response.wsgi_request)
        self.assertIn("You do no have access for this operation", list(map(lambda x: x.message, storage)))

