EMOJI_RED_CROSS = '\U0000274C'
EMOJI_SUCCESS = '\U0001F44D'

START = """I am a bot! \U0001F916
Please give me a command. I won't rebel. _For now_."""

HELP = r"""
This is the qBot, the bot to organize your queues. Here is a list of commands:
*Basic*:
    /help: show this help menu
    /start: start your conversation with the bot
*Queueing*:
    /queue: show queue
    /add [_element_]: add _element_ in the line. If no _element_ is provided, the user's username is added in the queue
    /next [_message_]: announce the first element of the queue with an optional message_
    /clear: clear queue
*Queue editing*:
    /rm _row-number_: remove the row from the list
    /insert _element_ _row-number_: insert _element_ in the specified row
"""

QUEUE_EMPTY = "The queue is currently empty"
ITEM_ALREADY_IN_QUEUE = EMOJI_RED_CROSS + " {item} is already in the queue at position {index}!"
ITEM_TOO_LONG = EMOJI_RED_CROSS + " '{item}' is too long. Please use less than {max_len} characters."

FORBIDDEN_ITEM_CHARACTERS = {'\n'}
FORBIDDEN_ITEM_MESSAGE = EMOJI_RED_CROSS + " Can't add {item} to the list: there is a forbidden character in your message"

ADD_SUCCESS = EMOJI_SUCCESS + " {item} added to the queue in position {index}"

CLEAR_SUCCESS = EMOJI_SUCCESS + " Queue cleared!"

RM_INDEX_NOT_PROVIDED =     EMOJI_RED_CROSS + " Please provide the row number that you want to delete, as in '/rm row'"
RM_TOO_MANY_ARGUMENTS =     EMOJI_RED_CROSS + " TMI! Please only provide the row number of the item you want to remove."
RM_INDEX_NOT_RECOGNIZED =   EMOJI_RED_CROSS + " I did not recognize '{index}' as a row number"
RM_INDEX_NOT_IN_QUEUE =     EMOJI_RED_CROSS + " Row {index} does not exist. Consult the queue with the command '/queue'"
RM_SUCCESS =                EMOJI_SUCCESS   + " Removed {item} from the queue"

INSERT_NOT_ENOUGH_ARGUMENTS =   EMOJI_RED_CROSS + " Please provide the item and the row where you want to insert the item, as in '/insert' row-number item"
INSERT_INDEX_NOT_RECOGNIZED =   RM_INDEX_NOT_RECOGNIZED
INSERT_INDEX_OUT_OF_BOUNDS =    EMOJI_RED_CROSS + " Row '{index}' is outside of the queue"
INSERT_QUEUE_EMPTY =            EMOJI_RED_CROSS + " Queue is currently empty. Please use '/add item' to add items in the queue before editing it!"
INSERT_SUCCESS =                EMOJI_SUCCESS   + " {item} inserted at position {index}"

NEXT_DEFAULT_MESSAGES = [
    "{item}, it's your time to shine! \U00002728",
    "{item}'s turn has finally arrived \U0001F389",
    "{item}: your wait is over! \U0000231B",
    "{item} has waited for long enough \U000023F0",
    "It's {item}'s turn \U0001F514"
]
NEXT_CUSTOM_REPLY = "{item}: {attached_message}"