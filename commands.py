import telegram
import random
import math
from functools import wraps
from utils import queue, messages
from utils.mwt import MWT


@MWT(timeout=60 * 60)
def _get_admin_ids(bot, chat_id):
    """Return a list of admin IDs. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


class Command:
    """Telegram command handler"""

    def __init__(self, update, context):
        self.update = update
        self.context = context

    @property
    def chat_type(self):
        return self.update.effective_chat.type

    @staticmethod
    def protected(permission, senderror=True):
        """Decorator to protect a command.
        Args:
            permission: function to evaluate the user permission. The argument
                of this function must be a Command object.
                Returns True if command can be executed.

            senderror: if True, a default error message is sent. Otherwise
                'permission' can send its own message
        """
        def protected_function(func):
            @wraps(func)
            def check_permissions(com, *args, **kwargs):
                if permission(com):
                    func(com, *args, *kwargs)
                else:
                    if senderror:
                        user = com.update.message.from_user.username
                        command = com.update.message.text
                        com.send(messages.PERMISSION_NOT_GRANTED, user=user,
                                 command=command)
            return check_permissions
        return protected_function

    def send_md(self, message, **kwformat):
        """Send a message in chat"""
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id,
            text=message.format(**kwformat),
            parse_mode=telegram.ParseMode.MARKDOWN,
        )

    def send(self, message, **kwformat):
        self.context.bot.send_message(
            chat_id=self.update.effective_chat.id,
            text=message.format(**kwformat)
        )

    def echo(self):
        """Echo the message"""
        self.send(self.update.message.text)

    def show_args(self):
        """Show arguments passed to the command"""
        answer = 'Your args:\n    ' + '\n    '.join(self.context.args)
        self.send(answer)

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


class BotFunction(Command):
    MAX_QUEUE_LINES = 25
    MAX_ITEM_LENGTH = 30

    def __init__(self, update, context):
        Command.__init__(self, update, context)
        chat_data = self.context.chat_data
        if 'queue' not in chat_data:
            self.context.chat_data['queue'] = queue.Queue()
        if 'is_frozen' not in chat_data:
            self.context.chat_data['is_frozen'] = True
        if 'is_protected' not in chat_data:
            self.context.chat_data['is_protected'] = True

    @property
    def queue(self):
        return self.context.chat_data['queue']

    def has_queue(self):
        """Return True if the chat has a queue"""
        return len(self.queue) > 0

    def clear_queue(self):
        """Clear queue"""
        self.queue.clear()

    @property
    def is_frozen(self):
        return self.context.chat_data['is_frozen']

    @is_frozen.setter
    def is_frozen(self, frozen):
        self.context.chat_data['is_frozen'] = frozen

    @property
    def is_protected(self):
        return self.context.chat_data['is_protected']

    @is_protected.setter
    def is_protected(self, protected):
        self.context.chat_data['is_protected'] = protected

    def check_not_frozen(self):
        if not self.is_frozen:
            # Chat not frozen
            return True
        else:
            return self.is_request_by_admin()

    def check_not_protected(self):
        # Group only
        if not self.is_protected:
            # Chat not protected
            return True
        else:
            # Command can be run only if requested by an admin
            return self.is_request_by_admin()

    @staticmethod
    def make_callable(bot_func):
        """Decorate a function with the standard signature as in
        f(update, context), then call it as a command"""

        def func_callable(update, context):
            bf = BotFunction(update, context)
            bfargs = bf.context.args
            return bot_func(bf, *bfargs)
        return func_callable

    def help(self, *args):
        self.send(messages.HELP)

    def start(self, *args):
        self.send(messages.START)

    def print_queue(self, *args):
        if self.has_queue():
            text = self.queue.format()
            # Check if test is too long
            if 1 + len(self.queue) > self.MAX_QUEUE_LINES:
                # Split the message into multiple submessages
                sections = text.split('\n')
                sub_msg_len = math.ceil(
                    (len(self.queue) + 1) / self.MAX_QUEUE_LINES
                )
                for i in range(sub_msg_len):
                    # Send each submessage on its own
                    start = i*self.MAX_QUEUE_LINES
                    end = min(len(sections), (i + 1)*self.MAX_QUEUE_LINES)
                    message = '\n  '.join(sections[start:end])
                    self.send(message)
            else:
                self.send(text)
        else:
            self.send(messages.QUEUE_EMPTY)

    @Command.protected(check_not_frozen)
    def add(self, *args):
        """Append an item in queue. This can be done only if the queue is not
        frozen."""
        if len(args) == 0:
            # No arguments: push user name into the list
            item = self.update.message.from_user.username
        else:
            # User asked for something specific. Check that the input doesn't
            # contain any forbidden character
            item = ' '.join(args)
            if any(forbidden_char in item for forbidden_char in
                   messages.FORBIDDEN_ITEM_CHARACTERS):
                self.send(messages.FORBIDDEN_ITEM_MESSAGE)
                return
            if len(item) > self.MAX_ITEM_LENGTH:
                self.send(messages.ITEM_TOO_LONG, item=item,
                          max_len=self.MAX_ITEM_LENGTH)
                return

        if item in self.queue:
            self.send(messages.ITEM_ALREADY_IN_QUEUE, item=item,
                      index=self.queue.index(item) + 1)
            return

        self.queue.append(item)
        if self.chat_type == telegram.Chat.PRIVATE:
            self.send(messages.ADD_SUCCESS_PRIVATE,
                      item=item, index=len(self.queue))
        else:
            user = self.update.message.from_user
            user = "{utag} ({uname})".format(uname=user.full_name,
                                             utag=user.username)
            self.send(messages.ADD_SUCCESS_GROUP, user=user, item=item,
                      index=len(self.queue))

    @Command.protected(check_not_protected)
    def next(self, *args):
        """Pick next turn"""
        if not self.has_queue():
            self.send(messages.QUEUE_EMPTY)
            return

        # Extract item from queue
        item, _ = self.queue.pop()

        # Generate reply
        if len(args) == 0:
            # Default reply
            attached_message = ''
            reply = random.choice(messages.NEXT_DEFAULT_MESSAGES)
        else:
            # Custom reply
            attached_message = ' '.join(args)
            reply = messages.NEXT_CUSTOM_REPLY
        self.send(reply, item=item, attached_message=attached_message)

    @Command.protected(check_not_protected)
    def clear(self, *args):
        self.clear_queue()
        self.send(messages.CLEAR_SUCCESS)

    @Command.protected(check_not_protected)
    def rm(self, *args):
        """Remove item at provided element in list"""
        if not self.has_queue():
            self.send(messages.QUEUE_EMPTY)
            return
        # Check (only the) index was provided
        if len(args) < 1:
            self.send(messages.RM_INDEX_NOT_PROVIDED)
            return
        elif len(args) > 1:
            self.send(messages.RM_TOO_MANY_ARGUMENTS)
            return

        # Check if index is a number
        index = args[0]
        if not index.isnumeric():
            self.send(messages.RM_INDEX_NOT_RECOGNIZED, index=index)
            return
        index = int(index)
        # Check if index is in range
        if index <= 0 or index > len(self.queue):
            self.send(messages.RM_INDEX_NOT_IN_QUEUE, index=index)
            return

        # Remove item and announce it
        item, _ = self.queue.remove(index - 1)
        self.send(messages.RM_SUCCESS, item=item)

    @Command.protected(check_not_frozen)
    def insert(self, *args):
        """Insert item in the list"""
        if not self.has_queue():
            self.send(messages.INSERT_QUEUE_EMPTY)
            return

        # Check arguments
        if len(args) < 2:
            self.send(messages.INSERT_NOT_ENOUGH_ARGUMENTS)
            return

        index = args[-1]
        item = args[:-1]
        item = ' '.join(item)
        # Check item
        if any([fc in item for fc in messages.FORBIDDEN_ITEM_CHARACTERS]):
            self.send(messages.FORBIDDEN_ITEM_MESSAGE)
            return
        if item in self.queue:
            self.send(messages.ITEM_ALREADY_IN_QUEUE, item=item,
                      index=self.queue.index(item) + 1)
            return

        # Check index
        if not index.isnumeric():
            self.send(messages.INSERT_INDEX_NOT_RECOGNIZED, index=index)
            return
        index = int(index)
        if index <= 0 or index > len(self.queue):
            self.send(messages.INSERT_INDEX_OUT_OF_BOUNDS, index=index)
            return

        # Insert item
        self.queue.insert(index - 1, item)
        if self.chat_type == telegram.Chat.PRIVATE:
            self.send(messages.INSERT_SUCCESS_PRIVATE,
                      item=item, index=len(self.queue))
        else:
            user = self.update.message.from_user
            user = "{utag} ({uname})".format(uname=user.full_name,
                                             utag=user.username)
            self.send(messages.INSERT_SUCCESS_GROUP, user=user, item=item,
                      index=len(self.queue))

    @Command.protected(Command.is_request_by_admin)
    def freeze(self, *args):
        """Freeze queue. Can only be requested by admins"""
        self.is_frozen = True
        self.send(messages.FREEZE_SUCCESS)

    @Command.protected(Command.is_request_by_admin)
    def unfreeze(self, *args):
        """Unfreeze queue. Can only be requested by admins"""
        self.is_frozen = False
        self.send(messages.UNFREEZE_SUCCESS)

    @Command.protected(Command.is_request_by_admin)
    def enable_protection(self, *args):
        self.is_protected = True
        self.send(messages.PROTECTION_ENABLED)

    @Command.protected(Command.is_request_by_admin)
    def disable_protection(self, *args):
        self.is_protected = False
        self.send(messages.PROTECTION_DISABLED)


COMMANDS = {
    # Debug commands
    # 'echo': echo,
    # 'showargs': show_args,
    'help':                 BotFunction.help,
    'start':                BotFunction.start,
    'queue':                BotFunction.print_queue,
    'add':                  BotFunction.add,
    'rm':                   BotFunction.rm,
    'insert':               BotFunction.insert,
    'next':                 BotFunction.next,
    'clear':                BotFunction.clear,
    'freeze':               BotFunction.freeze,
    'unfreeze':             BotFunction.unfreeze,
    'enable_protection':    BotFunction.enable_protection,
    'disable_protection':   BotFunction.disable_protection
}
