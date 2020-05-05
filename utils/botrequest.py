import telegram
from utils.mwt import MWT


class BotRequest:
    """Telegram bot requests handler"""
    def __init__(self, update, context):
        self.update = update
        self.context = context

    @property
    def chat_type(self):
        return self.update.effective_chat.type

    def send_md(self, message, **kwformat):
        """Send a message in chat with Markdown format"""
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id, text=message.format(**kwformat),
            parse_mode=telegram.ParseMode.MARKDOWN,
        )

    def send(self, message, **kwformat):
        """Send a non formatted message in chat"""
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id, text=message.format(**kwformat)
        )

    def is_request_by_admin(self):
        """Return true if request was sent from an admin - or if the chat is
        private."""
        # Private chats have no admins
        if self.chat_type in {telegram.Chat.GROUP, telegram.Chat.SUPERGROUP}:
            user_id = self.update.message.from_user.id
            bot = self.context.bot
            chat_id = self.update.effective_chat.id
            return user_id in _get_admin_ids(bot, chat_id)
        else:
            # It's a private chat
            return True


@MWT(timeout=60 * 60)
def _get_admin_ids(bot, chat_id):
    """Return a list of admin IDs. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
