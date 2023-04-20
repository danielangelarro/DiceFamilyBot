from telebot import TeleBot
from telebot.types import CallbackQuery

from tgbot.utils.transactions import accepted_deposite, remove_deposite


def autorized_retire_callback(call: CallbackQuery, bot: TeleBot):

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    user, money = accepted_deposite(message_id)
    text = f'❇️ Se ha aprobado su retiro ❇️\n\n💰 Saldo actual: ${money}'

    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(chat_id=user['id'], text=text)


def cancel_retire_callback(call: CallbackQuery, bot: TeleBot):

    chat_id = call.message.chat.id
    message_id = call.message.message_id

    user = remove_deposite(message_id)
    text = f'❌ Se ha rechazado su solicitud de retiro. ❌'
    
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(chat_id=user['id'], text=text)
