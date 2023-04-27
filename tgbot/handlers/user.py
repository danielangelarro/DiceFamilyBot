from telebot import TeleBot
from telebot.types import Message

import tgbot.config as config
from tgbot.callbacks.keyboards import games_keyboard, validate_deposite_keyboard
from tgbot.callbacks.reply_keyboard import reply_main_keyboard
from tgbot.utils.transactions import register_user, get_money, send_deposite


def any_user(message: Message, bot: TeleBot):
    """
    Users messages handlers.
    """

    register_user(message.from_user)

    text =  f'¡Bienvenido @{message.from_user.username} al Bot del Proyecto Dice! 🎲\n\n' \
            '😁¡Apostemos y divirtámonos!\n\n' \
            'Selecciona uno de nuestros tres juegos:\n' \
            '🎲 Dice Classic: adivina el número del dado.\n\n' \
            '📈 Tall & Bass: predice si el número será alto o bajo.\n\n' \
            '💣 DBomb: elige el dado que no saldrá.\n\n\n' \
            '¡Buena suerte!🍀'

    bot.send_message(message.chat.id, text=text, reply_markup=reply_main_keyboard)


def betting(message: Message, bot: TeleBot):

    chat_id = message.chat.id

    bot.send_dice(chat_id=chat_id, emoji='🎰')
    bot.send_message(chat_id=chat_id, text='**Selecciona un modo de juego**', reply_markup=games_keyboard(), parse_mode='MarkdownV2')


def my_account(message: Message, bot: TeleBot):

    chat_id = message.chat.id
    money = get_money(chat_id)

    sticker_id = 'CAACAgIAAxkBAAICcmRJxwz3TrpU92O88R9FT8l7jMNDAAIFAAMWbkwS9hEQhS3h0QwvBA'
    text =  '🎉 ¡Felicidades!\n\n' \
            f'Tu balance actual es de 💰 {money} 💰.\n' \
            '¡Sigue apostando y ganando! 💸💰🤑\n\n' \
            'No olvides apostar responsablemente. 🎲🃏✨\n\n' \
            '¡Que tengas un buen día! 😊'

    bot.send_sticker(chat_id, sticker_id)
    bot.send_message(chat_id, text)


def deposite_cash(message: Message, bot: TeleBot):

    chat_id = message.chat.id
    text = 'Envie una captura 🖼 de su transferencia y en la descripcion de la imagen coloque la cantidad a depositar.\n' \
            f'\n💳 Tarjeta a depositar: {config.TARJECT_CUP}'

    bot.send_message(chat_id=chat_id, text=text)


def support(message: Message, bot: TeleBot):

    chat_id = message.chat.id
    text = 'Escriba'

    bot.send_message(chat_id=chat_id, text=text)


def termine_and_conditions(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    text = 'Envie una captura 🖼 de su transferencia y en la descripcion de la imagen coloque la cantidad a depositar.\n' \
            f'\n💳 Tarjeta a depositar: {config.TARJECT_CUP}'

    bot.send_message(chat_id=chat_id, text=text)


def handle_photo(message: Message, bot: TeleBot):
    
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        photo_id = message.photo[-1].file_id
        money = message.caption

        caption = '\n\n' \
                f'👤 Usuario: @{message.from_user.username}\n' \
                f'🪪 Nombre: {message.from_user.full_name}\n' \
                f'💰 Dinero: {money}\n'

        bot.send_message(chat_id, f"FORMULARIO DE DEPÓSITO. {caption}")
        msg = bot.send_photo(chat_id=config.CHANNEL_PRIVATE_URL, photo=photo_id, caption=caption, 
                    parse_mode='Markdown', reply_markup=validate_deposite_keyboard())
        
        send_deposite(msg.message_id, float(money), user_id)
    
    except Exception as e:
        
        chat_id = message.chat.id

        print(e)

        bot.delete_message(chat_id, message.message_id)
        bot.send_message(chat_id, '⛔ Mensaje inválido. Vuelva a intentarlo.')
