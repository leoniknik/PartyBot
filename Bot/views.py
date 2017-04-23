from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('week')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def week(request):
    return render(request, 'week.html')


@login_required
def day(request, num):
    actives = Day.get_day_and_events(num)
    return render(request, 'day.html', {'actives': actives, 'num': num})


@login_required
def add_event(request, num):
    if request.method == 'GET':
        return render(request, 'add_event.html')
    elif request.method == 'POST':
        header = request.POST['header']
        description = request.POST['description']
        is_free = request.POST['is_free']
        if is_free == "true":
            is_free = True
        elif is_free == "false":
            is_free = False
        Event.add_event(header=header, description=description, is_free=is_free, num=num)
        return redirect('day', num=num)
