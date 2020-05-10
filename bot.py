from telegram.ext import Updater, CommandHandler, PicklePersistence
import logging
import botfunctions

PERSISTENCY = False


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
        exit(-1)
    if PERSISTENCY is True:
        # Make the bot persistent
        persistence = PicklePersistence(filename='persistence/data.pck',
                                        store_user_data=False, store_bot_data=False, store_chat_data=True)
        updater = Updater(token=token, use_context=True, persistence=persistence)
    else:
        updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    # Command handlers
    handlers = {}
    for command, func in botfunctions.COMMANDS.items():
        handler = CommandHandler(command, func)
        dispatcher.add_handler(handler)
        handlers[command] = handler
    # Logger
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater.start_polling()
    updater.idle()
