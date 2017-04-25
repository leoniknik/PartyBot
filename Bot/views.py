from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
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
    actives = Day.get_day_and_events(num, False)
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


@login_required
def edit_event(request, id, num):
    if request.method == 'GET':
        event = get_object_or_404(Event, id=id)
        return render(request, 'edit_event.html', {'event': event})
    elif request.method == 'POST':
        header = request.POST['header']
        description = request.POST['description']
        is_free = request.POST['is_free']
        if is_free == "true":
            is_free = True
        elif is_free == "false":
            is_free = False
        Event.objects.filter(id=id).update(header=header, description=description, is_free=is_free)
        return redirect('day', num=num)


@login_required
def delete_event(request, id, num):
    if request.method == 'GET':
        event = get_object_or_404(Event, id=id)
        return render(request, 'edit_event.html', {'event': event})
    elif request.method == 'POST':
        Event.objects.filter(id=id).delete()
        return redirect('day', num=num)


@login_required
def list_user(request):
    users = TelegramUser.objects.all().values('username', 'first_name', 'last_name', 'is_VIP', 'user_telegram_id')
    return render(request, 'list_user.html', {'users': users})


@login_required
def list_action(request):
    actions = Action.objects.all().values('user__username', 'user__first_name', 'message', 'time')
    return render(request, 'list_action.html', {'actions': actions})


@login_required
def change_vip(request, user_telegram_id):
    user = TelegramUser.objects.get(user_telegram_id=user_telegram_id)
    user.change_is_VIP()
    return redirect('list_user')


@login_required
def list_promotion(request):
    actions = Action.objects.all().values('user__username', 'user__first_name', 'message', 'time')
    return render(request, 'list_action.html', {'actions': actions})


@login_required
def add_promotion(request):
    actions = Action.objects.all().values('user__username', 'user__first_name', 'message', 'time')
    return render(request, 'list_action.html', {'actions': actions})


@login_required
def edit_promotion(request):
    actions = Action.objects.all().values('user__username', 'user__first_name', 'message', 'time')
    return render(request, 'list_action.html', {'actions': actions})


@login_required
def delete_promotion(request):
    actions = Action.objects.all().values('user__username', 'user__first_name', 'message', 'time')
    return render(request, 'list_action.html', {'actions': actions})
