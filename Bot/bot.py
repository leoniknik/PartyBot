# Hello, I'm party bot, I will be called from wsgi.py once
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Bot.models import TelegramUser, Action, Day, WeekDay
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ParseMode

updater = Updater(token='358413947:AAFRr2HUr7lc3rXPKp9XlrnFQ17r9aLG3b8')
dispatcher = updater.dispatcher

# TODO: for Kirill decorator

debug = False


def debug_print(item):
    if debug:
        print(item)


def start_command(bot, update):
    try:
        debug_print('start_command')
        debug_print('reg user now')
        TelegramUser.add_telegram_user(update.message.chat)
        debug_print('make keyboard')
        keyboard = [
            ['Пон', '..'],
            ['Вт', '..'],
            ['..']
        ]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
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
    0: 'Пон',
    1: 'Вт',
    2: 'Ср',
    3: 'Чт',
    4: 'Пт',
    5: 'Сб',
    6: 'Вс'
}
week_day_reverse_dict = {
    'Пон': 0,
    'Вт': 1,
    'Ср': 2,
    'Чт': 3,
    'Пт': 4,
    'Сб': 5,
    'Вс': 6
}


def echo(bot, update):
    try:
        debug_print('text')
        debug_print(update.message.text)
        Action.add_action(update.message)
        text = update.message.text
        debug_print(text)
        week_day_id = WeekDay(week_day_reverse_dict[text])
        week_day = WeekDay(week_day_id)
        debug_print(week_day)
        events = Day.get_day_and_events(week_day.value)
        debug_print(events)
        debug_print(events.count())
        if events.count() == 0:
            message = 'На ' + week_day_dict[int(week_day.value)] + ' мероприятий не запланировано'
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
        for event in events:
            message = ''
            message += '*' + event.header + '*' + '\n'
            message += event.description + '\n'
            rating = event.rating
            message += '*' + 'Рейтинг:' + str(rating) + '*'
            bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode=ParseMode.MARKDOWN)

    except KeyError as k_e:
        print(k_e)
        bot.sendMessage(chat_id=update.message.chat_id, text='не понимаю запрос')
    except Exception as ex:
        print(ex)


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

updater.start_polling()
