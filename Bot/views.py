from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            pass
            # Return a 'disabled account' error message
    else:
        # Return an 'invalid login' error message.
        pass


def signout(request):
    logout(request)
    # Redirect to a success page.


def signup(request):
    user = User.objects.create_user()
    user.save()
    # Redirect to a success page.
