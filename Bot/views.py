from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
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
    return render(request, 'day.html', {'actives': actives})
