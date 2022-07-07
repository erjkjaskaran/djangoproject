from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import auth_user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
# from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


def send_action_email(user, request):
    user = user
    current_site = get_current_site(request)
    email_subject = 'Activate Your Account'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])

    email.send(EmailMessage)


@auth_user_should_not_access
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "User not registered. Register your account")
            return render(request, 'authentication/registration.html')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.add_message(request, messages.ERROR, "Invalid Credentials")
            return render(request, 'authentication/login.html')

        if not user.is_email_verified:
            messages.add_message(request, messages.ERROR, "Email is not verified. Please check your inbox.")
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

        send_action_email( user, request)
        messages.add_message(request, messages.SUCCESS, "Account Created, you can now login")
        return render(request, 'authentication/login.html')

    return render(request, 'authentication/registration.html')


def logout_user(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,"Logged out Successfully")
    return redirect(reverse('login'))


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.object.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user):
        user.is_email_verified=True
        user.save()

        messages.add_message(request,messages.SUCCESS,'Email verified, you can now Login')
        return redirect(reverse('login'))

    return  render(request,'authentication/activate-failed.html')
