from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import auth_user_should_not_access


@auth_user_should_not_access
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.add_message(request, messages.ERROR, "Invalid Credentials")
            return render(request, 'authentication/login.html')
        login(request, user)

        messages.add_message(request, messages.SUCCESS, f"Welcome { user.username}")

        return redirect(reverse('home'))

    return render(request, 'authentication/login.html')


@auth_user_should_not_access
def register(request):
    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 8:
            messages.add_message(request, messages.ERROR, "Password should be atleast 8 characters")
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR, "Passwords mismatch")
            context['has_error'] = True
        if not validate_email(email):
            messages.add_message(request, messages.ERROR, "Enter a valid email address")
            context['has_error'] = True
        if not username:
            messages.add_message(request, messages.ERROR, "Username is required")
            context['has_error'] = True
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "Username is taken, Choose another one")
            context['has_error'] = True
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, "E-mail is taken, Choose another one")
            context['has_error'] = True
        if context['has_error']:
            return render(request, 'authentication/registration.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS, "Account Created, you can now login")
        return render(request, 'authentication/login.html')

    return render(request, 'authentication/registration.html')


def logout_user(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,"Logged out Successfully")
    return redirect(reverse('login'))