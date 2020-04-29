START = """I am a bot! \U0001F916
Please give me a command. I won't rebel. _For now_."""

HELP = """
This is the qBot, the bot to organize your queues. Here is a list of commands:
Basic:
    /help: show this help menu
    /start: start your conversation with the bot
Queueing:
    /queue: show queue
    /add [<element>]: add an element in the line. If no element
        is provided, the user's username is added in the queue.
    /next [<message>]: pick the first element in line and attach 
        an optional message
    /clear: clear queue
Queue editing:
    /rm <index>: remove the element under the provided index
    /insert <element> <position>: insert the element in the 
        specified index
"""

QUEUE_EMPTY = "The queue is currently empty"
ITEM_ALREADY_IN_QUEUE = "\U0000274C Item *{item}* is already in the queue at position {pos}!"

FORBIDDEN_ITEM_CHARACTERS = {'\n'}
FORBIDDEN_ITEM_MESSAGE = "Sorry, I can't add your item to the list: there is a forbidden character in your message."

NEXT_DEFAULT_MESSAGES = [
    "*{item}*, it's your time to shine! \U00002728",
    "*{item}*'s turn has finally arrived \U0001F389",
    "*{item}*: your wait is over! \U0000231B",
    "*{item}* has waited for long enough \U000023F0",
    "It's *{item}*'s turn \U0001F514"
]


def send(update, context, msg, **kwargs):
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, **kwargs)
