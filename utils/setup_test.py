from django.test import TestCase
from authentication.models import User
from faker import Faker

faker = Faker()
username = faker.name().split(" ")[0]
email = faker.email()
password = faker.paragraph(nb_sentences=5)


class TestSetup(TestCase):

    def setUp(self):
        print("Test Started")

    def create_todo(self):
        self.todo = {
            "title": faker.paragraph(nb_sentences=1),
            "description": faker.paragraph(nb_sentences=10)
        }
        return self.todo

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

    def tearDown(self):
        print('Test Finished')
        return super().tearDown()