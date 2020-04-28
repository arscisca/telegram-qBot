def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def show_args(update, context):
    answer = 'Your args:\n    ' + '\n    '.join(context.args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


COMMANDS = {
    'start': start,
    'echo': echo,
    'showargs': show_args
}