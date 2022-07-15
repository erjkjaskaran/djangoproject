from django.test import TestCase
from authentication.models import User
from faker import Faker
from django.urls import reverse
from todo.models import Todo

faker = Faker()
username = faker.name().split(" ")[0]
email = faker.email()
password = faker.paragraph(nb_sentences=1)


class TestSetup(TestCase):

    def setUp(self):
        print("Test Started")

    def create_todo(self):
        self.todo = {
            "title": faker.paragraph(nb_sentences=1),
            "description": faker.paragraph(nb_sentences=10)
        }
        return self.todo

    def create_todo_with_user(self, user):
        todo = self.create_todo()
        self.client.post(reverse('create-todo'), {
            'title': todo['title'],
            'description': todo['description'],
            'user': user
        })
        return Todo.objects.last()

    def register_user(self, username=username, email=email, password=password, password2=password):
        self.user = {
            "username": username,
            "email": email,
            "password": password,
            "password2": password2
        }
        return self.user

    def create_test_user(self, username=username, email=email, password=password):
        user = User.objects.create_user(username, email)
        user.set_password(password)
        user.is_email_verified = True
        user.save()
        return user

    def activate_user(self, username):
        user = User.objects.filter(username=username).first()
        user.is_email_verified = True
        user.save()
        return user

    def login(self, user2=None,passwrd=None):
        if user2!=None:
            user,password2=user2, passwrd
        else:
            user,password2=self.create_test_user(),password
        self.client.login(username=user.username, password=password2)
        return user

    def tearDown(self):
        print('Test Finished')
        return super().tearDown()