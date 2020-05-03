import telegram
import random
import math
from utils import queue, messages


class Command:
    """Telegram command handler"""

    def __init__(self, update, context):
        self.update = update
        self.context = context

    @property
    def queue(self):
        """Return the chat's Queue object"""
        return self.context.chat_data['queue']

    def has_queue(self):
        """Return True if the chat has a queue"""
        return 'queue' in self.context.chat_data

    def make_queue(self):
        """Assign a queue to the chat"""
        self.context.chat_data['queue'] = queue.Queue()

    def clear_queue(self):
        """Remove the queue from the chat"""
        if self.has_queue():
            self.context.chat_data.pop('queue')

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


class BotFunction(Command):
    MAX_QUEUE_LINES = 25
    MAX_ITEM_LENGTH = 30
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
        self.send_md(messages.START)

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

    def add(self, *args):
        """Append an item in queue"""
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

        if not self.has_queue():
            self.make_queue()

        if item in self.queue:
            self.send(
                messages.ITEM_ALREADY_IN_QUEUE, item=item,
                index=self.queue.index(item) + 1)
        else:
            self.queue.append(item)
            self.send(messages.ADD_SUCCESS, item=item, index=len(self.queue))

    def next(self, *args):
        """Pick next turn"""
        if not self.has_queue():
            self.send(messages.QUEUE_EMPTY)
            return

        # Extract item from queue
        item, _ = self.queue.pop()
        if len(self.queue) == 0:
            self.clear_queue()

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

    def clear(self, *args):
        self.clear_queue()
        self.send(messages.CLEAR_SUCCESS)

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
        if len(self.queue) == 0:
            self.clear_queue()
        self.send(messages.RM_SUCCESS, item=item)

    def insert(self, *args):
        """Insert item in the list"""
        if not self.has_queue():
            self.send(messages.INSERT_QUEUE_EMPTY)

        # Check arguments
        if len(args) < 2:
            self.send(messages.INSERT_NOT_ENOUGH_ARGUMENTS)
            return

        index, *item = args
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
        self.send(messages.INSERT_SUCCESS, item=item,
                  index=self.queue.index(item) + 1)


COMMANDS = {
    # Debug commands
    # 'echo': echo,
    # 'showargs': show_args,
    'help':     BotFunction.help,
    'start':    BotFunction.start,
    'queue':    BotFunction.print_queue,
    'add':      BotFunction.add,
    'rm':       BotFunction.rm,
    'insert':   BotFunction.insert,
    'next':     BotFunction.next,
    'clear':    BotFunction.clear
}
