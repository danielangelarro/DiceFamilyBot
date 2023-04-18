from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from tgbot.utils.transactions import validate_transaction, register_user

    
def admin_user(message: Message, bot: TeleBot):
    
    register_user(message.from_user)
    bot.send_message(message.chat.id, "Hello, admin!")


def validate_transaction_by_admin(message: Message, bot: TeleBot):
    
    chat_id = message.chat.id
    message_id = message.id
    
    msg = [line.split(':') for line in message.text.split('\n')]
    ID, USER, GAME, MONEY, TIME = [data[1].strip() for data in msg[1:]]

    validate_transaction(ID)
    text = f'**Se ha aceptado su apuesta.**\n\nJuego: {GAME}\nCantidad: {MONEY}\nHora: {TIME}'

    bot.delete_message(chat_id, message_id)
    bot.send_message(USER, text, parse_mode='Markdown')
