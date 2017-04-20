#Hello, I'm party bot, I will be called from wsgi.py once
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater(token='358413947:AAFRr2HUr7lc3rXPKp9XlrnFQ17r9aLG3b8')
dispatcher = updater.dispatcher


def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    print(error)


def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


unknown_handler = MessageHandler(Filters.command, unknown)
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(unknown_handler)
dispatcher.add_error_handler(error)
dispatcher.add_handler(echo_handler)

updater.start_polling()
