from telebot import TeleBot
from telebot.types import Message, MessageEntity, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import tgbot.config as config
from tgbot.utils.transactions import GAMES, send_money, get_money
from tgbot.callbacks.keyboards import dice_keyboard, tall_and_bass_keyboard, dbomb_keyboard


BOT = None
GAME = None
NUMBER = None


def select_game_callback(call: CallbackQuery, bot: TeleBot):

    game = call.data[6:]
    text =  f'{game}\n\n' \
            f"**Seleccione la opción a la que desea apostar:**"

    if game == GAMES[0]:

        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=dice_keyboard(), parse_mode='MarkdownV2')

    elif game == GAMES[1]:

        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=tall_and_bass_keyboard(), parse_mode='MarkdownV2')
    
    elif game == GAMES[2]:

        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=dbomb_keyboard(), parse_mode='MarkdownV2')

    # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def dice_callback(call: CallbackQuery, bot: TeleBot):

    global BOT, GAME, NUMBER
    BOT = bot
    GAME = GAMES[0]
    NUMBER = int(call.data[5])

    bot.send_message(call.message.chat.id, '**Introduzca la cantidad de dinero a apostar:**', parse_mode='MarkdownV2')
    bot.register_next_step_handler(call.message, process_betting_step)

    # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def tall_and_bass_callback(call: CallbackQuery, bot: TeleBot):

    global BOT, GAME, NUMBER
    BOT = bot
    GAME = GAMES[1]
    NUMBER = 1 if call.data == 'tb-bass' else 6

    bot.send_message(call.message.chat.id, '**Introduzca la cantidad de dinero a apostar:**', parse_mode='MarkdownV2')
    bot.register_next_step_handler(call.message, process_betting_step)

    # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def dbomb_callback(call: CallbackQuery, bot: TeleBot):

    global BOT, GAME, NUMBER
    BOT = bot
    GAME = GAMES[2]
    NUMBER = int(call.data[6])

    bot.send_message(call.message.chat.id, '**Introduzca la cantidad de dinero a apostar:**', parse_mode='MarkdownV2')
    bot.register_next_step_handler(call.message, process_betting_step)

    # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def process_betting_step(message: Message):
    
    global BOT, GAME, NUMBER


    try:
        user = message.from_user.id
        chat_id = message.chat.id
        message_id = message.message_id

        money = float(message.text)
        money_db = get_money(user)


        if money <= 0 or money > money_db:
            
            raise ValueError('Cantidad de dinero a apostar inválida.')

        text = '🎟 BOLETO DICE 🎟\n\n' \
               f'👤 Usuario: @{message.from_user.username}\n' \
               f'🪪 Nombre: {message.from_user.full_name}\n' \
               f'🎲 Juego: {GAME}\n' \
               f'🔮 Prediccion: {NUMBER}\n' \
               f'💰 Dinero: {money}\n\n#predict'

        msg = BOT.send_message(chat_id=config.CHANNEL_PRIVATE_URL, text=text)
        send_money(msg.message_id, user, NUMBER, money, GAME)
        
        BOT.send_message(chat_id=chat_id, text=text)
        BOT.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    except Exception as e:

        print(e)
        BOT.reply_to(message, '⛔ Error de envío.')
