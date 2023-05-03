from telebot import TeleBot
from telebot.types import Message

import tgbot.config as config
from tgbot.callbacks.keyboards import validate_retire_keyboard
from tgbot.utils.transactions import get_money, send_deposite


def retire_cash(message: Message, bot: TeleBot):

    user = message.from_user.id
    chat_id = message.chat.id
    money = get_money(user)

    if money < 120:

        text = '❌ Su saldo es insufuciente para efectuar un retiro. ❌\nDebe tener más de 120 CUP.'
        bot.send_message(chat_id=chat_id, text=text)

        return

    text = 'Introduzca la cantidad de dinero a retirar. Debe ser mayor que $120:'

    mensaje = bot.send_message(message.chat.id, text)
    mensaje_id = mensaje.message_id
    db_user = {'msg':mensaje_id, 'name':message.from_user.username, 'tarject':'', 'phone':'', 'money':0}

    bot.register_next_step_handler(mensaje, money_step, bot, db_user)


def money_step(message: Message, bot: TeleBot, db_user: dict):

    try:
        money = float(message.text)
        user = message.from_user.id
        chat_id = message.chat.id
        total_money = get_money(user) - money

        if total_money < 0 or money < 120:
            raise ValueError('Dinero Insuficiente')

        db_user['money'] = money
        text = f"Introduzca su numero de tarjeta CUP:"

        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=db_user['msg'], text=text)
        bot.register_next_step_handler(message, tarjet_step, bot, db_user)
    
    except Exception as e:

        bot.reply_to(message, '❌ No se pudo efectuar el retiro. Verifique que los datos sean correctos.')


def tarjet_step(message: Message, bot: TeleBot, db_user: dict):

    try:
        chat_id = message.chat.id
        db_user['tarject'] = message.text
        text = f"Introduzca su número de teléfono:"

        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=db_user['msg'], text=text)
        bot.register_next_step_handler(message, phone_step, bot, db_user)
    
    except Exception as e:

        bot.reply_to(message, '❌ No se pudo efectuar el retiro. Verifique que los datos sean correctos.')


def phone_step(message: Message, bot: TeleBot, db_user: dict):

    try:
        chat_id = message.chat.id
        db_user['phone'] = message.text

        plantilla = "🎟 SOLICITUD RETIRO 🎟\n\n" \
                    f"👤 Usuario: @{db_user['name']}\n" \
                    f"💳 Tarjeta: {db_user['tarject']}\n" \
                    f"📱 Teléfono: {db_user['phone']}\n" \
                    f"💰 Cantidad: {db_user['money']}\n\n" \

        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=db_user['msg'], text=plantilla)

        msg = bot.send_message(chat_id=config.CHANNEL_PRIVATE_URL, text=plantilla,
                        parse_mode='MarkdownV2', reply_markup=validate_retire_keyboard())
        
        send_deposite(msg.message_id, db_user['money'], message.from_user.id)
    
    except Exception as e:

        print(e)

        text = '❌ No se pudo efectuar el retiro. Verifique que los datos sean correctos.'
        bot.edit_message_text(chat_id=message.chat.id, message_id=db_user['msg'], text=text)
