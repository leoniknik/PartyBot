from django.db import models
from datetime import date
from django.utils import timezone
from enum import Enum
from django.db.models import Max
from telegram import ParseMode


class Day(models.Model):
    name = models.CharField(verbose_name='day', max_length=255, default="")
    week_day_id = models.IntegerField(verbose_name='week_day_id', default=-1)
    date = models.DateField(verbose_name='date', default=date.fromordinal(1))
    actual = models.BooleanField(verbose_name='actual', default=True)

    @staticmethod
    def get_day_and_events(week_day, free_mode):
        day = Day.objects.get(actual=True, week_day_id=week_day)
        return day.get_events(free_mode=free_mode)

    def get_events(self, free_mode):
        if free_mode:
            return Event.objects.filter(day_id=self.id, is_free=True)
        else:
            return Event.objects.filter(day_id=self.id)

    @staticmethod
    def get_day_and_top_events(week_day, free_mode):
        day = Day.objects.get(actual=True, week_day_id=week_day)
        return day.get_top_events(free_mode=free_mode)

    def get_top_events(self, free_mode):
        if free_mode:
            max_rate = Event.objects.filter(
                day_id=self.id, is_free=True
            ).aggregate(max_rate=Max('rating'))['max_rate']
            events = Event.objects.filter(day_id=self.id, is_free=True, rating=max_rate)
        else:
            max_rate = Event.objects.filter(
                day_id=self.id
            ).aggregate(max_rate=Max('rating'))['max_rate']
            events = Event.objects.filter(day_id=self.id, rating=max_rate)
        if len(events) != 0:
            return events[0]
        else:
            return None

    @staticmethod
    def get_actual_day(week_day):
        return Day.objects.get(actual=True, week_day_id=week_day)


class TelegramUser(models.Model):
    username = models.TextField(verbose_name='username', default="")
    first_name = models.TextField(verbose_name='first_name', default="")
    last_name = models.TextField(verbose_name='last_name', default="")
    user_telegram_id = models.BigIntegerField(verbose_name='id', primary_key=True)
    free_mode = models.BooleanField(verbose_name='free_mode', default=False)
    is_VIP = models.BooleanField(verbose_name='is_VIP', default=False)

    @staticmethod
    def add_telegram_user(chat):
        user = TelegramUser()
        user.username = chat['username']
        user.first_name = chat['first_name']
        user.last_name = chat['last_name']
        user.user_telegram_id = chat['id']
        user.save()
        return TelegramUser.objects.get(user_telegram_id=chat['id'])

    @staticmethod
    def get_user(chat):
        return TelegramUser.objects.get(user_telegram_id=chat['id'])

    @staticmethod
    def get_all_users():
        return TelegramUser.objects.all()

    def change_is_VIP(self):
        if self.is_VIP:
            self.is_VIP = False
        else:
            self.is_VIP = True
        self.save()


class Action(models.Model):
    message = models.TextField(verbose_name='message', default="")
    time = models.DateTimeField()
    user = models.ForeignKey(TelegramUser, null=True)

    @staticmethod
    def add_action(message):
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

    @staticmethod
    def get_all_events_by_day(num):
        day = Day.get_actual_day(num)
        events = Event.objects.filter(day=day).order_by('id')
        return events

    @staticmethod
    def get_event(id):
        try:
            return Event.objects.get(id=id)
        except Exception as e:
            print(e)

    def get_ability_to_vote(self, user):
        if 0 != len(Vote.objects.filter(event_id=self.id, user_id=user.user_telegram_id)):
            return False
        else:
            return True


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
            event.save()
            vote.save()
        except Exception as ex:
            print(ex)


class BotMessage(models.Model):
    message_id = models.BigIntegerField(verbose_name='id', primary_key=True)
    chat_id = models.BigIntegerField(verbose_name='chat_id', default=-1)
    text = models.TextField(verbose_name='text', default="")
    event = models.ForeignKey(Event, null=True)


    @staticmethod
    def make_message(event):
        message = ''
        message += '*' + event.header + '*' + '\n'
        message += event.description + '\n'
        rating = event.rating
        message += '' + 'Рейтинг: ' + str(rating) + ''
        return message


    @staticmethod
    def delete_old_messages(bot, event,message):
            old_messages = BotMessage.objects.filter(event_id=event.id, chat_id=message.chat_id)
            for old_message in old_messages:
                if True:
                    try:
                        text=''
                        try:
                            text=BotMessage.make_message(event=event)
                        except Exception:
                            pass
                        bot.editMessageText(text=text, chat_id=old_message.chat_id,
                                            message_id=old_message.message_id, parse_mode=ParseMode.MARKDOWN)
                    except Exception as ex:
                        print(ex)

    @staticmethod
    def send_message(bot, update, message, parse_mode, reply_markup, event,silent):
        log = bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode=parse_mode,
                              reply_markup=reply_markup,disable_notification=silent)
        bot_msg = BotMessage()
        bot_msg.text = message
        bot_msg.chat_id = update.message.chat_id
        bot_msg.message_id = log.message_id
        bot_msg.event = event
        bot_msg.save()


class WeekDay(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6


class Advertisement(models.Model):
    text = models.TextField(verbose_name='text', default="")

    @staticmethod
    def add_advertisement(text):
        try:
            advertisement = Advertisement()
            advertisement.text = text
            advertisement.save()
        except Exception as ex:
            print(ex)
