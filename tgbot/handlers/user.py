import random
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, Dice
from tgbot.utils.transactions import GAMES, register_user, get_money
from tgbot.callbacks.keyboards import games_keyboard

def any_user(message: Message, bot: TeleBot):
    """
    Users messages handlers.
    """

    register_user(message.from_user)

    text = f'Hola {message.from_user.full_name}. Predice el número y recibe ganacias. Qué esperas??!!'

    bot.send_message(message.chat.id, text=text)


def betting(message: Message, bot: TeleBot):

    chat_id = message.chat.id

    bot.send_dice(chat_id=chat_id, emoji='🎰')
    bot.send_message(chat_id=chat_id, text='**Selecciona un modo de juego**', reply_markup=games_keyboard())


def my_account(message: Message, bot: TeleBot):

    chat_id = message.chat.id
    money = get_money(chat_id)
    text = f'Su cuenta tiene: ${money}'

    bot.send_message(chat_id, text)