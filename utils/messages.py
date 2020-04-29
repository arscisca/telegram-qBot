START = """I am a bot! \U0001F916
Please give me a command. I won't rebel. _For now_."""

HELP = """
This is the qBot, the bot to organize your queues. Here is a list of commands:
Basic:
    /help: show this help menu
    /start: start your conversation with the bot
    /stop: stop the bot
Queueing:
    /queue: show queue
    /add <element>: add an element in the line
    /next [<message>]: pick the first element in line and attach 
        an optional message
    /clear: clear queue
Queue editing:
    /rm <index>: remove the element under the provided index
    /insert <element> <position>: insert the element in the 
        specified index
"""


def send(update, context, msg, **kwargs):
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, **kwargs)
