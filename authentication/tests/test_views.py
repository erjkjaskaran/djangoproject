from django.urls import reverse
from django.contrib.messages import get_messages
from utils.setup_test import TestSetup
from authentication.models import User


class TestViews(TestSetup):

    def test_should_show_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "authentication/registration.html")

    def test_should_show_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authentication/login.html")

    def test_should_sign_up_user(self):
        user = self.register_user()
        response = self.client.post(reverse("register"), user)
        self.assertEqual(response.status_code,200)
        storage = get_messages(response.wsgi_request)
        self.assertIn("Account Created, you can now login", list(map(lambda x: x.message, storage)))

    def test_should_not_sign_up_user_with_taken_username(self):
        user1 = self.register_user(email="email@gmail.com")
        user2 = self.register_user(email="email2@gmail.com")
        self.client.post(reverse("register"), user1)
        response = self.client.post(reverse("register"), user2)
        self.assertEqual(response.status_code,409)
        storage=get_messages(response.wsgi_request)
        self.assertIn("Username is taken, Choose another one", list(map(lambda x: x.message, storage)))

    def test_should_not_sign_up_user_with_taken_email(self):
        user1 = self.register_user(username="user")
        user2 = self.register_user(username="user2")
        self.client.post(reverse("register"), user1)
        response = self.client.post(reverse("register"), user2)
        self.assertEqual(response.status_code,409)
        storage = get_messages(response.wsgi_request)
        self.assertIn("E-mail is taken, Choose another one", list(map(lambda x: x.message, storage)))

    def test_should_not_sign_up_user_if_passwords_mismatch(self):
        user = self.register_user(password="password", password2="password2")
        response = self.client.post(reverse("register"), user)
        self.assertEqual(response.status_code, 409)
        storage = get_messages(response.wsgi_request)
        self.assertIn("Passwords mismatch", list(map(lambda x: x.message, storage)))

    def test_should_login_user(self):
        user = self.register_user()
        self.client.post(reverse("register"), user)
        activated_user = self.activate_user(user['username'])
        response = self.client.post(reverse('login'), {'username': activated_user.username, 'password': user['password']})
        storage = get_messages(response.wsgi_request)
        self.assertIn(f"Welcome {activated_user.username}", list(map(lambda x: x.message, storage)))
        self.assertEqual(response.status_code, 302)

    def test_should_not_login_user_with_email_not_verified(self):
        user = self.register_user()
        self.client.post(reverse("register"), user)
        response = self.client.post(reverse('login'), user)
        storage = get_messages(response.wsgi_request)
        self.assertIn("Email is not verified. Please check your inbox.", list(map(lambda x: x.message, storage)))
        self.assertEqual(response.status_code, 409)