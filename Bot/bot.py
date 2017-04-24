# Hello, I'm party bot, I will be called from wsgi.py once
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from Bot.models import TelegramUser, Action, Day, WeekDay,Event,Vote,BotMessage
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ParseMode
import time

updater = Updater(token='358413947:AAFRr2HUr7lc3rXPKp9XlrnFQ17r9aLG3b8')
dispatcher = updater.dispatcher

# TODO: for Kirill decorator

debug = False


def debug_print(item):
    if debug:
        print(item)


def get_keyboard(_chat):
    user = TelegramUser.get_user(_chat)
    keyboard = [[]]
    if user.free_mode:
        keyboard = [
            ['Понедельник', 'Вторник'],
            ['Среда', 'Четверг'],
            ['Пятница', 'Суббота'],
            ['Воскресенье'],
            ['Все', 'Популярное']
        ]
    else:
        keyboard = [
            ['Понедельник', 'Вторник'],
            ['Среда', 'Четверг'],
            ['Пятница', 'Суббота'],
            ['Воскресенье'],
            ['Бесплатно', 'Популярное']
        ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

def start_command(bot, update):
    try:
        debug_print('start_command')
        debug_print('reg user now')
        TelegramUser.add_telegram_user(update.message.chat)
        debug_print('make keyboard')

        markup = get_keyboard(update.message.chat)
        update.message.reply_text('Привет:', reply_markup=markup)
    except Exception as ex:
        print(ex)


def help_command(bot, update):
    print('help_command')
    bot.sendMessage(chat_id=update.message.chat_id, text='help text')


command_dict = {
    "/start": start_command,
    "/help": help_command
}

week_day_dict = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье'
}
week_day_reverse_dict = {
    'Понедельник': 0,
    'Вторник': 1,
    'Среда': 2,
    'Четверг': 3,
    'Пятница': 4,
    'Субботаб': 5,
    'Воскресенье': 6
}


def echo(bot, update):
   text=update.message.text
   if text=='Популярное':
       send_message_top(bot=bot,update=update)
   elif text=='Бесплатно' or text=='Все':
       switch_free_mode(bot=bot,update=update)
   else:
       send_message_by_week_day(bot=bot,update=update)

def switch_free_mode(bot, update):
    user=TelegramUser.get_user(update.message.chat)
    user.free_mode= not user.free_mode
    user.save()
    markup = get_keyboard(update.message.chat)
    if user.free_mode:
        update.message.reply_text('Показывать только бесплатные события', reply_markup=markup)
    else:
        update.message.reply_text('Показывать все события', reply_markup=markup)


def send_message_by_week_day(bot, update):
    try:
        debug_print('text')
        user = TelegramUser.get_user(update.message.chat)
        debug_print(update.message.text)
        Action.add_action(update.message)
        text = update.message.text
        debug_print(text)
        week_day_id = WeekDay(week_day_reverse_dict[text])
        week_day = WeekDay(week_day_id)
        debug_print(week_day)
        events = Day.get_day_and_events(week_day.value,user.free_mode)


        event_col = len(events)#.count()


        if event_col == 0:
            message = 'На ' + week_day_dict[int(week_day.value)] + ' мероприятий не запланировано'
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
        else:


            BotMessage.delete_old_messages(bot=bot,update=update,events=events)
            for i in range(0, event_col):
                event = events[i]

                message = make_message(event)
                reply_markup = get_inline_keyboard(event=event, user=user)
                BotMessage.send_message(bot=bot, update=update, message=message, parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=reply_markup, event=event)
                if i != (event_col - 1):
                    time.sleep(1)

                #if i != (event_col - 1):
                #    #bot.sendMessage(chat_id=update.message.chat_id, disable_notification=True, text=message,
                #    #                parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
                #    BotMessage.send_message(bot=bot,update=update,message=message,parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup,event=event)
#
                #    time.sleep(1)
                #else:
                #    bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode=ParseMode.MARKDOWN,
                #                    reply_markup=reply_markup)
#



    except KeyError as k_e:
        print(k_e)
        bot.sendMessage(chat_id=update.message.chat_id, text='не понимаю запрос')
    except Exception as ex:
        print(ex)

def send_message_top(bot, update):
    try:
        debug_print('text')
        user = TelegramUser.get_user(update.message.chat)
        debug_print(update.message.text)
        Action.add_action(update.message)
        text = update.message.text
        events=[]
        for i in range(0,7):
            event=Day.get_day_and_top_events(i,user.free_mode)
            if(event is not None):
                events.append((i,event))
        debug_print(events)
        event_col = len(events)
        print(event_col)

        if event_col == 0:
            message = 'Мероприятия не найдены'
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
        else:

            BotMessage.delete_old_messages(bot=bot,update=update,events=events)
            for i in range(0, event_col):
                event = events[i][1]
                week_day_id=events[i][0]

                message = make_message(event)
                message = '*' + week_day_dict[week_day_id] + '*' + '\n\n'+message
                reply_markup = get_inline_keyboard(event=event, user=user)

                BotMessage.send_message(bot=bot, update=update, message=message, parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=reply_markup, event=event)
                if i != (event_col - 1):
                    #bot.sendMessage(chat_id=update.message.chat_id, disable_notification=True, text=message,
                    #                parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

                    time.sleep(1)
                #else:
                    #bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode=ParseMode.MARKDOWN,
                    #                reply_markup=reply_markup)

    except KeyError as k_e:
        print(k_e)
        bot.sendMessage(chat_id=update.message.chat_id, text='не понимаю запрос')
    except Exception as ex:
        print(ex)

def get_inline_keyboard(event, user):
    if event.get_ability_to_vote(user):
        return get_filled_inline_keyboard(event)
    else:
        return get_empty_inline_keyboard()

def make_message(event):
    message = ''
    message += '*' + event.header + '*' + '\n\n'
    message += event.description + '\n\n'
    rating = event.rating
    message += '*' + 'Рейтинг:' + str(rating) + '*'
    return message

def get_filled_inline_keyboard(event):
    keyboard = [[InlineKeyboardButton("+", callback_data=str(str(event.id) + '#^*_1')),
                 InlineKeyboardButton("-", callback_data=str(str(event.id) + '#^*_0'))]]

    return InlineKeyboardMarkup(keyboard)

def get_empty_inline_keyboard():
    keyboard = [[]]
    return InlineKeyboardMarkup(keyboard)












def button(bot, update):


    query = update.callback_query
    query_data_tuple=get_data_tuple(query.data)

    event=Event.get_event(query_data_tuple[0])
    user=TelegramUser.get_user(update.callback_query.message.chat)
    print(query_data_tuple[1])




    if query_data_tuple[1]==1:
        type=True
    else:
        type=False

    if event.get_ability_to_vote(user=user):
        Vote.add_vote(type_of_vote=type,event=event,user=user)


    event = Event.get_event(query_data_tuple[0])

    message=make_message(event)
    reply_markup = get_empty_inline_keyboard()


    bot.editMessageText(text=message,chat_id=query.message.chat_id,message_id=query.message.message_id, parse_mode=ParseMode.MARKDOWN,reply_markup=reply_markup)

def get_data_tuple(query_data):
    ind = query_data.index('#^*_')
    data1=int(query_data[:ind])
    data2=int(query_data[ind+4:])
    return (data1,data2)











def error(bot, update, error):
    print(error)


def command(bot, update):
    try:
        print('command')
        print(update.message.text)
        Action.add_action(update.message)
        func = command_dict[update.message.text]
        func(bot, update)
    except KeyError as k_e:
        print(k_e)
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command")
    except Exception as ex:
        print(ex)
        bot.sendMessage(chat_id=update.message.chat_id, text="System error")


command_handler = MessageHandler(Filters.command, command)
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(command_handler)
dispatcher.add_error_handler(error)
dispatcher.add_handler(echo_handler)

updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
