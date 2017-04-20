from django.db import models


class Day(models.Model):
    name = models.CharField(verbose_name='day', max_length=255, default="")


class TelegramUser(models.Model):
    username = models.TextField(verbose_name='username', default="")
    first_name = models.TextField(verbose_name='first_name', default="")
    last_name = models.TextField(verbose_name='last_name', default="")
    user_telegram_id = models.BigIntegerField(verbose_name='id', primary_key=True)


class Action(models.Model):
    message = models.TextField(verbose_name='message', default="")
    time = models.DateTimeField()
    user = models.ForeignKey(TelegramUser, null=True)


class Event(models.Model):
    header = models.TextField(verbose_name='header', default="")
    description = models.TextField(verbose_name='description', default="")
    is_free = models.BooleanField(verbose_name='is_free', default=True)
    rating = models.IntegerField(verbose_name='rating', default=0)
    day = models.ForeignKey(Day, null=True)


class Vote(models.Model):
    type = models.BooleanField(verbose_name='vote', default=True)
    event = models.ForeignKey(Event, null=True)
    user = models.ForeignKey(TelegramUser, null=True)
