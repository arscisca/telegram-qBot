from telegram.ext import Updater, CommandHandler
import logging
import commands


def read_token(fname):
    try:
        f = open(fname, 'r')
    except OSError:
        return None
    else:
        with f:
            line = f.readline()
            key = line.strip()
            return key


if __name__ == "__main__":
    # Setup updater
    token = read_token('.token')
    if token is None:
        print("Bot token was not found in file '{}'".format('.token'))
    updater = Updater(token='1100753787:AAEAdkJq4PLgjiyhBIlzk00IhMWmI7y_sdI', use_context=True)
    dispatcher = updater.dispatcher
    # Command handlers
    handlers = {}
    for command, func in commands.COMMANDS.items():
        handler = CommandHandler(command, func)
        dispatcher.add_handler(handler)
        handlers[command] = handler
    # Logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater.start_polling()
