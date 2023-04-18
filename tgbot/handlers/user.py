from telebot import TeleBot
from telebot.types import Message

import tgbot.config as config
from tgbot.callbacks.keyboards import games_keyboard, validate_deposite_keyboard
from tgbot.utils.transactions import register_user, get_money, send_deposite


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


def deposite_cash(message: Message, bot: TeleBot):

    chat_id = message.chat.id
    text = 'Envie una captura 🖼 de su transferencia y en la descripcion de la imagen coloque la cantidad a depositar.'

    bot.send_message(chat_id=chat_id, text=text)


def handle_photo(message: Message, bot: TeleBot):
    
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        photo_id = message.photo[-1].file_id
        money = message.caption

        caption = '**Depósito**\n\n' \
                f'👤 Usuario: @{message.from_user.username}\n' \
                f'🪪 Nombre: {message.from_user.full_name}\n' \
                f'💰 Dinero: {money}\n'

        bot.send_message(chat_id, f"Usted ha solicitado depositar ${caption}. SU cuenta sera confirmada.")
        msg = bot.send_photo(chat_id=config.CHANNEL_PRIVATE_URL, photo=photo_id, caption=caption, 
                    parse_mode='Markdown', reply_markup=validate_deposite_keyboard())
        
        send_deposite(msg.message_id, float(money), user_id)
    
    except Exception as e:
        
        chat_id = message.chat.id

        print(e)

        bot.delete_message(chat_id, message.message_id)
        bot.send_message(chat_id, '⛔ Mensaje inválido. Vuelva a intentarlo.')