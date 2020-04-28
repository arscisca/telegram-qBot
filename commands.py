import telegram


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, I'm happy to help you organize your group! I promise I won't take over the world. _For now_.",
        parse_mode=telegram.ParseMode.MARKDOWN
    )


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
