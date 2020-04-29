EMOJI_RED_CROSS = '\U0000274C'
EMOJI_SUCCESS = '\U00002714'

START = """I am a bot! \U0001F916
Please give me a command. I won't rebel. _For now_."""

HELP = """
This is the qBot, the bot to organize your queues. Here is a list of commands:
*Basic*:
   /help: show this help menu
   /start: start your conversation with the bot
*Queueing*:
    /queue: show queue
    /add [_element_]: add an element in the line. If no element
        is provided, the user's username is added in the queue.
    /next [_message_]: pick the first element in line and attach 
        an optional message
    /clear: clear queue
*Queue editing*:
    /rm _row_: remove the element on the provided row number
    /insert <element> <row>: insert the element in the 
        specified row
"""

QUEUE_EMPTY = "The queue is currently empty"
ITEM_ALREADY_IN_QUEUE = EMOJI_RED_CROSS + " *{item}* is already in the queue at position {index}!"

FORBIDDEN_ITEM_CHARACTERS   = {'\n'}
FORBIDDEN_ITEM_MESSAGE      = EMOJI_RED_CROSS + "Sorry, I can't add your item to the list: " \
                                                "there is a forbidden character in your message."

RM_INDEX_NOT_PROVIDED   = EMOJI_RED_CROSS + \
                        " Please provide the index of the item to remove within the command, as in " \
                        "'/rm <index-of-the-item>'!"
RM_TOO_MANY_ARGUMENTS   = EMOJI_RED_CROSS + \
                          " TMI! Please only provide the integer index of the item you want to remove."
RM_INDEX_NOT_RECOGNIZED = EMOJI_RED_CROSS + " I did not recognize '_{index}_' as a row number"
RM_INDEX_NOT_IN_QUEUE   = EMOJI_RED_CROSS + " There's nothing under index _{index}_. Consult the queue with the " \
                                            "command '/queue'"
RM_SUCCESS = EMOJI_SUCCESS + " Removed *{item}* from the queue"


INSERT_NOT_ENOUGH_ARGUMENTS = EMOJI_RED_CROSS + " Please provide the index where you want the new item inserted and the" \
                                                "item itself, as in '/insert <index> <item>'"
INSERT_INDEX_NOT_RECOGNIZED = RM_INDEX_NOT_RECOGNIZED
INSERT_INDEX_OUT_OF_BOUNDS = EMOJI_RED_CROSS + " Index '_{index}_' is outside of the queue. Please insert a vailid " \
                                               "row number."
INSERT_SUCCESS = EMOJI_SUCCESS + " *{item}* inserted at position {index}"


NEXT_DEFAULT_MESSAGES = [
    "*{item}*, it's your time to shine! \U00002728",
    "*{item}*'s turn has finally arrived \U0001F389",
    "*{item}*: your wait is over! \U0000231B",
    "*{item}* has waited for long enough \U000023F0",
    "It's *{item}*'s turn \U0001F514"
]


def send(update, context, msg, **kwargs):
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, **kwargs)
