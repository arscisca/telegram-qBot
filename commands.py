import telegram
import utils.queue as queue


def create_queue(context):
    context.chat_data['queue'] = queue.Queue()


def clear_queue(context):
    context.chat_data.pop('queue')


def has_queue(context):
    return 'queue' in context.chat_data


def send_msg(update, context, msg):
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, I'm happy to help you organize your group! I promise I won't take over the world. _For now_.",
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def stop(update, context):
    clear_queue(context)


def echo(update, context):
    send_msg(update, context, update.message.text)


def show_args(update, context):
    answer = 'Your args:\n    ' + '\n    '.join(context.args)
    send_msg(update, context, answer)


def print_queue(update, context):
    if has_queue(context):
        send_msg(update, context, context.chat_data['queue'].format())
    else:
        send_msg(update, context, 'The queue is empty')


def append(update, context):
    """Append an item in queue"""
    if not has_queue(context):
        create_queue(context)
    item = ' '.join(context.args)

    q = context.chat_data['queue']
    q.append(item)
    send_msg(update, context, "{} added to queue in position {}".format(item, q.index(item) + 1))


def next(update, context):
    """Pick next turn"""
    if not has_queue(context):
        send_msg(update, context, 'The queue is empty')
        return

    queue = context.chat_data['queue']

    item, _ = queue.pop()
    if len(queue) == 0:
        clear_queue(context)

    attached = ' '.join(context.args)
    message = "{}: ".format(item)
    if not attached:
        attached = "it's your turn!"
    send_msg(update, context, message + attached)


def clear(update, context):
    clear_queue(context)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Queue cleared')


COMMANDS = {
    # Debug commands
    # 'echo': echo,
    # 'showargs': show_args,

    'start': start,
    'stop': stop,
    'queue': print_queue,
    'append': append,
    'next': next,
    'clear': clear
}
