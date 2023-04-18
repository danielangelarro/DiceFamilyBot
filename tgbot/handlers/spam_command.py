from telebot import TeleBot
from telebot.types import Message


def anti_spam(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """
    if bot.temp_data:
        if bot.temp_data.get(message.from_user.id) != 'OK':
            return
    bot.send_message(
        message.chat.id,
        """This is demo spam command.
If you send this command more than once within 2 seconds, 
bot will warn you.
This is made by using middlewares."""
)


def wrap_group(message: Message, bot: TeleBot):

    text = f'{message.chat.id} - {message.chat.title}'

    print(text)

    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
