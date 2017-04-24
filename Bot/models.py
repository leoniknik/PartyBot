from django.db import models
from datetime import date
from django.utils import timezone
from enum import Enum


class Day(models.Model):
    name = models.CharField(verbose_name='day', max_length=255, default="")
    week_day_id = models.IntegerField(verbose_name='week_day_id', default=-1)
    date = models.DateField(verbose_name='date', default=date.fromordinal(1))
    actual = models.BooleanField(verbose_name='actual', default=True)

    @staticmethod
    def get_day_and_events(week_day):
        day = Day.objects.get(actual=True, week_day_id=week_day)
        return day.get_events()

    def get_events(self):
        return Event.objects.filter(day_id=self.id)

    @staticmethod
    def get_actual_day(week_day):
        return Day.objects.get(actual=True, week_day_id=week_day)


class TelegramUser(models.Model):
    username = models.TextField(verbose_name='username', default="")
    first_name = models.TextField(verbose_name='first_name', default="")
    last_name = models.TextField(verbose_name='last_name', default="")
    user_telegram_id = models.BigIntegerField(verbose_name='id', primary_key=True)

    @staticmethod
    def add_telegram_user(chat):
        print('new user')
        print(chat)
        user = TelegramUser()
        user.username = chat['username']
        user.first_name = chat['first_name']
        user.last_name = chat['last_name']
        user.user_telegram_id = chat['id']
        user.save()
        return TelegramUser.objects.get(user_telegram_id=chat['id'])


class Action(models.Model):
    message = models.TextField(verbose_name='message', default="")
    time = models.DateTimeField()
    user = models.ForeignKey(TelegramUser, null=True)

    @staticmethod
    def add_action(message):
        # if (message.text == '/start'):
        #     return None
        try:
            action = Action()
            action.user_id = message.chat['id']
            action.message = message.text
            action.time = timezone.now()
            action.save()
        except Exception as ex:
            print(ex)


class Event(models.Model):
    header = models.TextField(verbose_name='header', default="")
    description = models.TextField(verbose_name='description', default="")
    is_free = models.BooleanField(verbose_name='is_free', default=True)
    rating = models.IntegerField(verbose_name='rating', default=0)
    day = models.ForeignKey(Day, null=True)

    @staticmethod
    def add_event(header, description, is_free, num):
        try:
            event = Event()
            event.header = header
            event.description = description
            event.is_free = is_free
            event.rating = 0
            event.day = Day.get_actual_day(num)
            event.save()
        except Exception as e:
            print(e)

        # def get_rating(self):
        #    plus = Vote.objects.filter(event_id=self.id, type=True).count()
        #    minus = Vote.objects.filter(event_id=self.id, type=False).count()
        #    return (plus - minus)


class Vote(models.Model):
    type = models.BooleanField(verbose_name='vote', default=True)
    event = models.ForeignKey(Event, null=True)
    user = models.ForeignKey(TelegramUser, null=True)

    @staticmethod
    def add_vote(type_of_vote, event, user):
        try:
            vote = Vote()
            vote.event = event
            vote.user = user
            vote.type = type_of_vote
            event.rating += 1 if type_of_vote else -1
            vote.save()
        except Exception as ex:
            print(ex)


class WeekDay(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6
