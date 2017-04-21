#Hello, I'm party bot, I will be called from wsgi.py once
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from Bot.models import TelegramUser,Action,Day,WeekDay
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,ParseMode


updater = Updater(token='358413947:AAFRr2HUr7lc3rXPKp9XlrnFQ17r9aLG3b8')
dispatcher = updater.dispatcher
debug = False
def dprint(item):
    if debug:print(item)






def start_command(bot,update):
    dprint('start_command')
    dprint('reg user now')
    TelegramUser.add_telegram_user(update.message.chat)
    dprint('make keyboard')
    try:

        kb= [['Пон', '..'],
            ['Вт', '..'],
            ['..']]
        markup = ReplyKeyboardMarkup(kb, one_time_keyboard=False)
        update.message.reply_text('Привет:', reply_markup=markup)


    except Exception as ex:
        print(ex)

def help_command(bot,update):
    print('help_command')
    bot.sendMessage(chat_id=update.message.chat_id, text='help text')



command_dict={
    "/start":start_command,
    "/help":help_command
}

week_day_dict={
    0:'Пон',
    1:'Вт',
    2:'Ср',
    3:'Чт',
    4:'Пт',
    5:'Сб',
    6:'Вс'
}
week_day_rev_dict={
    'Пон':0,
    'Вт':1,
    'Ср':2,
    'Чт':3,
    'Пт':4,
    'Сб':5,
    'Вс':6
}

def echo(bot, update):
    dprint('text')
    dprint(update.message.text)
    Action.add_Action(update.message)
    text=update.message.text
    try:
        dprint(text)
        week_day_id=WeekDay(week_day_rev_dict[text])
        week_day=WeekDay(week_day_id)
        dprint(week_day)
        events=Day.get_day_and_events(week_day)
        dprint(events)
        dprint(events.count())
        if events.count()==0:
            message='На '+week_day_dict[week_day.value] +' мероприятий не запланировано'
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
        for event in events:
            message=''
            message+='*'+event.header+'*'+'\n'
            message += event.description + '\n'
            rating=event.get_rating()
            message += '*'+'Рейтинг:'+str(rating)+'*'
            bot.sendMessage(chat_id=update.message.chat_id, text=message,parse_mode=ParseMode.MARKDOWN)

    except KeyError as k_e:
        print(k_e)
        bot.sendMessage(chat_id=update.message.chat_id, text='не понимаю запрос')
    except Exception as ex:
        print(ex)



def error(bot, update, error):
    print(error)


def command(bot, update):
    print('command')
    print(update.message.text)
    Action.add_Action(update.message)

    try:
        func = command_dict[update.message.text]
        func(bot, update)
    except KeyError as k_e:
        print(k_e)
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
    except Exception as ex:
        print(ex)
        bot.sendMessage(chat_id=update.message.chat_id, text="System error.")


    #bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

command_handler = MessageHandler(Filters.command, command)
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(command_handler)
dispatcher.add_error_handler(error)
dispatcher.add_handler(echo_handler)

updater.start_polling()
