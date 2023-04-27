from telebot import TeleBot
from telebot.types import Message
from tgbot.utils.transactions import register_user
from tgbot.callbacks.reply_keyboard import reply_main_keyboard
from tgbot.utils.validators import validate_join_channel

    
def admin_user(message: Message, bot: TeleBot):

    register_user(message.from_user)

    text =  f'¡Bienvenido @{message.from_user.username} al Bot del Proyecto Dice! 🎲\n\n' \
            '😁¡Apostemos y divirtámonos!\n\n' \
            'Selecciona uno de nuestros tres juegos:\n' \
            '🎲 Dice Classic: adivina el número del dado.\n\n' \
            '📈 Tall & Bass: predice si el número será alto o bajo.\n\n' \
            '💣 DBomb: elige el dado que no saldrá.\n\n\n' \
            '¡Buena suerte!🍀'

    bot.send_message(message.chat.id, text, reply_markup=reply_main_keyboard())


def groups_info_admin(message: Message, bot: TeleBot):

    # ID del canal que quieres obtener
    channel_id = "@BoletosDice"

    # Utiliza el método get_chat para obtener la información del canal
    channel_info = bot.get_chat(channel_id)

    # Imprime la información del canal
    text =  f'ID del canal: {channel_info.id}\n' \
            f'Nombre del canal: {channel_info.title}\n' \
            f'Descripción del canal: {channel_info.description}'

    bot.send_message(message.chat.id, text=text)
    bot.send_message(channel_id, "Hola, ¡soy un nuevo miembro del canal!")


    # # Utiliza el método get_chat_member para obtener información sobre el bot en el canal
    # bot_info = bot.get_chat_member(channel_id, bot.)

    # # Utiliza el método promote_chat_member para darle al bot permisos de administrador en el canal
    # bot.promote_chat_member(
    #     channel_id, bot_info.user.id, 
    #     can_change_info=True, 
    #     can_post_messages=True, 
    #     can_edit_messages=True, 
    #     can_delete_messages=True, 
    #     can_invite_users=True, 
    #     can_restrict_members=True, 
    #     can_pin_messages=True, 
    #     can_promote_members=False
    # )
    # # Envia un mensaje al canal


def info_messaje_by_admin(message: Message, bot: TeleBot):

    text = str(message)
    text = text.replace(',', '\n')
    
    # user = message.from_user

    bot.reply_to(message, message.sticker.file_id)
    # bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAPMZEA03cwetuxrTS20VEwFc117CNMAApEDAAIvD_AGA79Grv8Gf-8vBA')
