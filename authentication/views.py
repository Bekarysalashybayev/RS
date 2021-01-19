from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.template import loader


def send_sms(email, key) -> bool:
    data = "" + str(key)
    send_mail('Welcome to StudyShare!', data, "no-reply@study-share.info",
              [email], fail_silently=False)
    return True


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid username or password')
            return redirect("/login")
    else:
        return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return redirect('/login')

    return render(request, 'register.html')


def logout(request):
    auth_logout(request)
    return redirect('/')


def home(request):
    if request.method == 'POST':
        name = request.POST['Name']
        email = request.POST['Email']
        send_sms("bekarysalashybaev@gmail.com", "Имя: " + name + "\n Почта: " + email)
        return redirect('/')
    users = User.objects.all()
    context = {
        'list': users
    }
    html_template = loader.get_template('home.html')
    return HttpResponse(html_template.render(context, request))
