import telegram
from utils import queue, messages


def create_queue(context):
    context.chat_data['queue'] = queue.Queue()


def clear_queue(context):
    if has_queue(context):
        context.chat_data.pop('queue')


def has_queue(context):
    return 'queue' in context.chat_data


def start(update, context):
    messages.send(update, context, messages.START, parse_mode=telegram.ParseMode.MARKDOWN)


def stop(update, context):
    clear_queue(context)


def echo(update, context):
    messages.send(update, context, update.message.text)


def show_args(update, context):
    answer = 'Your args:\n    ' + '\n    '.join(context.args)
    messages.send(update, context, answer)


def print_queue(update, context):
    if has_queue(context):
        messages.send(update, context, context.chat_data['queue'].format())
    else:
        messages.send(update, context, 'The queue is empty')


def add(update, context):
    """Append an item in queue"""
    if not has_queue(context):
        create_queue(context)
    item = ' '.join(context.args)

    q = context.chat_data['queue']
    q.append(item)
    messages.send(update, context, "{} added to queue in position {}".format(item, q.index(item) + 1))


def next(update, context):
    """Pick next turn"""
    if not has_queue(context):
        messages.send(update, context, 'The queue is empty')
        return

    queue = context.chat_data['queue']

    item, _ = queue.pop()
    if len(queue) == 0:
        clear_queue(context)

    attached = ' '.join(context.args)
    message = "{}: ".format(item)
    if not attached:
        attached = "it's your turn!"
    messages.send(update, context, message + attached)


def clear(update, context):
    clear_queue(context)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Queue cleared')


def bot_help(update, context):
    messages.send(update, context, messages.HELP)

COMMANDS = {
    # Debug commands
    # 'echo': echo,
    # 'showargs': show_args,
    'help': bot_help,
    'start': start,
    'stop': stop,
    'queue': print_queue,
    'add': add,
    'next': next,
    'clear': clear
}
