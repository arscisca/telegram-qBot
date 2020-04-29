import telegram
import random
from utils import queue, messages


def create_queue(context):
    """Make a new queue for the chat context"""
    context.chat_data['queue'] = queue.Queue()


def clear_queue(context):
    """Delete the queue from chat context"""
    if has_queue(context):
        context.chat_data.pop('queue')


def has_queue(context):
    """Return True if chat context already has a queue"""
    return 'queue' in context.chat_data


def start(update, context):
    """Send starting message"""
    messages.send(update, context, messages.START, parse_mode=telegram.ParseMode.MARKDOWN)


def echo(update, context):
    """Echo the message"""
    messages.send(update, context, update.message.text)


def show_args(update, context):
    """Show arguments passed to the command"""
    answer = 'Your args:\n    ' + '\n    '.join(context.args)
    messages.send(update, context, answer)


def print_queue(update, context):
    """Print the queue"""
    if has_queue(context):
        messages.send(update, context, context.chat_data['queue'].format())
    else:
        messages.send(update, context, messages.QUEUE_EMPTY)


def add(update, context):
    """Append an item in queue"""
    if len(context.args) == 0:
        # No arguments: push user name into the list
        item = update.message.from_user.username
    else:
        # User asked for something specific. Check that the input doesn't
        # contain any forbidden character
        item = ' '.join(context.args)
        if any(forbidden_char in item for forbidden_char in messages.FORBIDDEN_ITEM_CHARACTERS):
            messages.send(update, context, messages.FORBIDDEN_ITEM_MESSAGE)
            return

    if not has_queue(context):
        create_queue(context)

    q = context.chat_data['queue']
    if item in q:
        messages.send(
            update, context, messages.ITEM_ALREADY_IN_QUEUE.format(item=item, index=q.index(item) + 1),
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    else:
        q.append(item)
        messages.send(
            update, context,
            messages.EMOJI_SUCCESS + " *{}* added to queue in position {}".format(item, len(q)),
            parse_mode=telegram.ParseMode.MARKDOWN
        )


def next(update, context):
    """Pick next turn"""
    if not has_queue(context):
        messages.send(update, context, messages.QUEUE_EMPTY)
        return
    q = context.chat_data['queue']

    # Extract item from queue
    item, _ = q.pop()
    if len(q) == 0:
        clear_queue(context)

    # Generate reply
    if len(context.args) == 0:
        # Default reply
        reply = random.choice(messages.NEXT_DEFAULT_MESSAGES).format(item=str(item))
    else:
        # Custom reply
        custom_message = ' '.join(context.args)
        reply = "*{item}* : {custom_message}".format(item=str(item), custom_message=custom_message)
    messages.send(update, context, reply, parse_mode=telegram.ParseMode.MARKDOWN)


def clear(update, context):
    """Clear queue"""
    clear_queue(context)
    messages.send(update, context, messages.EMOJI_SUCCESS + ' Queue cleared!')


def rm(update, context):
    """Remove item at provided element in list"""
    if not has_queue(context):
        messages.send(update, context, messages.QUEUE_EMPTY)
        return
    # Check (only the) index was provided
    if len(context.args) < 1:
        # Index not provided
        messages.send(update, context, messages.RM_INDEX_NOT_PROVIDED, parse_mode=telegram.ParseMode.MARKDOWN)
        return
    elif len(context.args) > 1:
        # Too many arguments
        messages.send(update, context, messages.RM_TOO_MANY_ARGUMENTS, parse_mode=telegram.ParseMode.MARKDOWN)
        return

    index = context.args[0]
    if not index.isnumeric():
        messages.send(
            update, context,
            messages.RM_INDEX_NOT_RECOGNIZED.format(index=index),
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        return

    q = context.chat_data['queue']
    index = int(index)
    if index == 0 or index > len(q):
        messages.send(
            update, context,
            messages.RM_INDEX_NOT_IN_QUEUE.format(index=index),
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        return
    item, _ = q.remove(index - 1)
    if len(q) == 0:
        clear_queue(context)
    messages.send(update, context, messages.RM_SUCCESS.format(item=item), parse_mode=telegram.ParseMode.MARKDOWN)


def bot_help(update, context):
    """Print help"""
    messages.send(update, context, messages.HELP)


COMMANDS = {
    # Debug commands
    # 'echo': echo,
    # 'showargs': show_args,
    'help': bot_help,
    'start': start,
    'queue': print_queue,
    'add': add,
    'rm': rm,
    'next': next,
    'clear': clear
}
