from django.db import models
from datetime import date
from django.utils import timezone
from enum import Enum


class Day(models.Model):
    name = models.CharField(verbose_name='day', max_length=255, default="")
    week_day_id=models.IntegerField(verbose_name='week_day_id',default=-1)
    date = models.DateField(verbose_name='date', default=date.fromordinal(1))
    actual = models.BooleanField(verbose_name='actual', default=True)

    @staticmethod
    def get_day_and_events(week_day):
        week_day_code=week_day.value
        day=Day.objects.get(actual=True,week_day_id=week_day_code)
        return day.get_events()

    def get_events(self):
        return Event.objects.filter(day_id=self.id)


class TelegramUser(models.Model):
    username = models.TextField(verbose_name='username', default="")
    first_name = models.TextField(verbose_name='first_name', default="")
    last_name = models.TextField(verbose_name='last_name', default="")
    user_telegram_id = models.BigIntegerField(verbose_name='id', primary_key=True)


    @staticmethod
    def add_telegram_user(chat):
        print('new user')
        print(chat)
        new_user=TelegramUser()
        new_user.username=chat['username']
        new_user.first_name=chat['first_name']
        new_user.last_name=chat['last_name']
        new_user.user_telegram_id=chat['id']
        new_user.save()
        return TelegramUser.objects.get(user_telegram_id=chat['id'])


class Action(models.Model):
    message = models.TextField(verbose_name='message', default="")
    time = models.DateTimeField()
    user = models.ForeignKey(TelegramUser, null=True)

    @staticmethod
    def add_Action(message):
        if(message.text=='/start'):
            return None
        try:
            new_action=Action()
            new_action.user_id=message.chat['id']
            new_action.message=message.text
            new_action.time=timezone.now()
            new_action.save()
        except Exception as ex:
            print(ex)


class Event(models.Model):
    header = models.TextField(verbose_name='header', default="")
    description = models.TextField(verbose_name='description', default="")
    is_free = models.BooleanField(verbose_name='is_free', default=True)
    rating = models.IntegerField(verbose_name='rating', default=0) #не нужное поле, тк нарушает нормализацию
    day = models.ForeignKey(Day, null=True)

    def get_rating(self):
        plus=Vote.objects.filter(event_id=self.id,type=True).count()
        minus=Vote.objects.filter(event_id=self.id,type=False).count()
        return (plus-minus)

class Vote(models.Model):
    type = models.BooleanField(verbose_name='vote', default=True)
    event = models.ForeignKey(Event, null=True)
    user = models.ForeignKey(TelegramUser, null=True)

class WeekDay(Enum):
    Monday=0
    Tuesday=1
    Wednesday=2
    Thursday=3
    Friday=4
    Saturday=5
    Sunday=6
