EMOJI_RED_CROSS = '\U0000274C'
EMOJI_SUCCESS = '\U0001F44D'
EMOJI_FROZEN = '\U0001F9CA'
EMOJI_LOCK = '\U0001F512'
EMOJI_OPEN_LOCK = '\U0001F513'

START = """I am a bot! \U0001F916
Please give me a command. I won't rebel. For now.
Type '/help' for a list of commands"""

HELP = """
This is the qBot, the bot to organize your queues. Here is a list of
commands:
Basic:
    /help: show this help menu
    /start: start your conversation with the bot

Queueing:
    /queue: show queue
    /add [item]: add item to the line. If no item is provided, 
        the user's username is added in the queue
    /next [message]: announce the first element of the queue 
        with an optional message
    /clear: clear queue
        
Queue editing:
    /rm row-number: remove the row from the list
    /insert item row-number: insert item in the specified row

For group admins:
    Group admins can always run any command, even when the 
    queue is frozen. They also have the following commands 
    available:
    
    \U0001F512 /enable_protection: non-admins can only run /help, 
                /add, /queue
    \U0001F512 /disable_protection:
    \U0001F512 /freeze: freeze queue. Items can't be added or 
                 inserted until /unfreeze is requested
    \U0001F512 /unfreeze: unfreeze queue
    
    \U0001F512: Admins only in group chat, available in
                private chats.
"""

QUEUE_EMPTY = "The queue is currently empty"
ITEM_ALREADY_IN_QUEUE = EMOJI_RED_CROSS + " {item} is already in the queue at position {index}!"
ITEM_TOO_LONG = EMOJI_RED_CROSS + " '{item}' is too long. Please use less than {max_len} characters."
PERMISSION_NOT_GRANTED = EMOJI_LOCK + " Sorry {user}, you don't have the permission to '{command}'"

FORBIDDEN_ITEM_CHARACTERS = {'\n'}
FORBIDDEN_ITEM_MESSAGE = EMOJI_RED_CROSS + " Can't add {item} to the list: there is a forbidden character in your message"

ADD_SUCCESS_PRIVATE = EMOJI_SUCCESS + " {item} added to the queue in position {index}"
ADD_SUCCESS_GROUP = EMOJI_SUCCESS + " {user} added '{item}' to the queue at position {index}"
ADD_QUEUE_FROZEN = EMOJI_FROZEN + " Can't add '{item}': queue is frozen! Run '/unfreeze' to unfreeze it"

CLEAR_SUCCESS = EMOJI_SUCCESS + " Queue cleared!"

RM_INDEX_NOT_PROVIDED =     EMOJI_RED_CROSS + " Please provide the row number that you want to delete, as in '/rm row'"
RM_TOO_MANY_ARGUMENTS =     EMOJI_RED_CROSS + " TMI! Please only provide the row number of the item you want to remove."
RM_INDEX_NOT_RECOGNIZED =   EMOJI_RED_CROSS + " I did not recognize '{index}' as a row number"
RM_INDEX_NOT_IN_QUEUE =     EMOJI_RED_CROSS + " Row {index} does not exist. Consult the queue with the command '/queue'"
RM_SUCCESS =                EMOJI_SUCCESS   + " Removed {item} from the queue"

INSERT_NOT_ENOUGH_ARGUMENTS =   EMOJI_RED_CROSS + " Please provide the item and the row where you want to insert the item, as in '/insert item row-number'"
INSERT_INDEX_NOT_RECOGNIZED =   RM_INDEX_NOT_RECOGNIZED
INSERT_INDEX_OUT_OF_BOUNDS =    EMOJI_RED_CROSS + " Row '{index}' is outside of the queue"
INSERT_QUEUE_EMPTY =            EMOJI_RED_CROSS + " Queue is currently empty. Please use '/add item' to add items in the queue before editing it!"
INSERT_QUEUE_FROZEN =           EMOJI_FROZEN + " Can't insert '{item}': queue is frozen! Run '/unfreeze' to unfreeze it"
INSERT_SUCCESS_PRIVATE =        EMOJI_SUCCESS + " {item} inserted at position {index}"
INSERT_SUCCESS_GROUP =          EMOJI_SUCCESS + " {user} inserted '{item}' at position {index}"

FREEZE_NOT_AN_ADMIN = EMOJI_RED_CROSS + " Sorry, you don't have the permission: only admins can freeze the queue!"
FREEZE_SUCCESS = EMOJI_FROZEN + " Queue frozen!"

UNFREEZE_NOT_AN_ADMIN = EMOJI_RED_CROSS + " Sorry, you don't have the permission: only admins can unfreeze the queue!"
UNFREEZE_SUCCESS = "\U0001F525 Queue unfrozen!"

PROTECTION_ENABLED = EMOJI_LOCK + " Protection enabled!"
PROTECTION_DISABLED = EMOJI_OPEN_LOCK + " Protection disabled!"
NEXT_DEFAULT_MESSAGES = [
    "{item}, it's your time to shine! \U00002728",
    "{item}'s turn has finally arrived \U0001F389",
    "{item}: your wait is over! \U0000231B",
    "{item} has waited for long enough \U000023F0",
    "It's {item}'s turn \U0001F514"
]
NEXT_CUSTOM_REPLY = "{item}: {attached_message}"