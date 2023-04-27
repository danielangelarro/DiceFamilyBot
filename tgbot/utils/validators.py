from telebot import TeleBot
from telebot.types import User, InlineKeyboardButton, InlineKeyboardMarkup
import tgbot.config as config
import time


def validate_join_channel(user: User, bot: TeleBot):

    if not bot.get_chat_member(chat_id=config.CHANNEL_PUBLIC_URL, user_id=user.id):

        invite = bot.create_chat_invite_link(config.CHANNEL_PRIVATE_URL, member_limit=1)
        InviteLink = invite.invite_link #Get the actual invite link from 'invite' class
        
        text = f"Hola {user.first_name}\. Presiona *CLICK* en el siguiente boton para unirte a nuestro canal\."
        mrkplink = InlineKeyboardMarkup() #Created Inline Keyboard Markup
        mrkplink.add(InlineKeyboardButton("Unirse 🚀", url=InviteLink)) #Added Invite Link to Inline Keyboard
        
        bot.send_message(user.id, text, reply_markup=mrkplink, parse_mode='MarkdownV2')
        
        return False
    
    return True