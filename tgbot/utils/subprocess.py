
import time, random
from telebot import TeleBot
from datetime import datetime

import tgbot.config as config
from .transactions import db, GAMES


def is_win(intents, number):

    intens = [int(i) for i in intents.split()]

    return number in intents


def filter_bettings(bot: TeleBot, bettings, number):

    win, error, = [], []

    for tr in bettings:

        if not tr['autorized']:
            
            bot.delete_message(chat_id=config.CHANNEL_PRIVATE_URL, message_id=tr['id'])
            error.append(tr)

        elif is_win(tr['numbers'], number):

            win.append(tr)
    
    return win, error


def submit_message_channel(bot: TeleBot, win: int, number: int):

    state = 'Bass' if number <= 3 else 'Tall'

    text = f'''🏆Resultado🏆 
            {number}

 ✅Estado: {state}

🥇Ganadores:  {len(win)} 

💵Participa: https://t.me/+lf_NopzgGjZlODcx 

💰MULTIPLICADOR💰

Dice Classic: x{config.DICE_MULTIPLIER}

Tall and Bass: x{config.TALL_MULTIPLIER}

DBomb: x{config.DBOMB_MULTIPLIER}'''

    bot.send_dice(chat_id=config.CHANNEL_PUBLIC_URL, emoji='🎲')
    bot.send_message(chat_id=config.CHANNEL_PUBLIC_URL, text=text)


def submit_message_pv(bot: TeleBot, dice, tall, dbomb, error):

    for w in dice:
        user = db.get_user_by_id(w['user'])

        money = float(w['money'] * config.DICE_MULTIPLIER)
        db.set_user(money, user['id'])

        text = "Usted ha ganado.\n*Juego:* Dice Clasic\n*Dinero:* {money}"
        bot.send_message(chat_id=user['id'], text=text, parse_mode='Markdown')
    
    for w in tall:
        user = db.get_user_by_id(w['user'])

        money = float(w['money'] * config.DICE_MULTIPLIER)
        db.set_user(money, user['id'])

        text = "Usted ha ganado.\n*Juego:* Tall and Bass\n*Dinero:* {money}"
        bot.send_message(chat_id=user['id'], text=text, parse_mode='Markdown')
    
    for w in dbomb:
        user = db.get_user_by_id(w['user'])

        money = float(w['money'] * config.DICE_MULTIPLIER)
        db.set_user(money, user['id'])

        text = "Usted ha ganado.\n*Juego:* DBomb\n*Dinero:* {money}"
        bot.send_message(chat_id=user['id'], text=text, parse_mode='Markdown')

    for w in error:
        user = db.get_user_by_id(w['user'])
        text = 'Lo sentimos. Su apuesta no fue aprobada a tiempo.'
        bot.send_message(chat_id=user['id'], text=text, parse_mode='Markdown')


def submit_message_manager(bot: TeleBot, win, error):

    dice, tall, dbomb = [], [], []

    for w in win:

        user = db.get_user_by_id(w['user'])

        if w['game'] == GAMES[0]:

            dice.append(f"{user['user']} - {user['name']} - ${user['money']}")
        
        elif w['game'] == GAMES[1]:

            dice.append(f"{user['user']} - {user['name']} - ${user['money']}")
        
        else:

            dice.append(f"{user['user']} - {user['name']} - ${user['money']}")
    
    submit_message_pv(bot, dice, tall, dbomb, error)
    dice, tall, dbomb = '\n'.join(dice), '\n'.join(tall), '\n'.join(dbomb)
    
    text = f"🏆Resultado🏆\n**Dice Classic:**\n{dice}\n\n**Tall and Bass:**\n{tall}\n\n**DBomb:**\n{dbomb}"
    bot.send_message(chat_id=config.CHANNEL_PRIVATE_URL, text=text)


def async_game(bot: TeleBot):
     
    band = True

    while True:

        time.sleep(1)        

        if datetime.now().minute == 0:

            if not band:

                continue

            band = False

            bettings = db.get_bettings()
            db.remove_all_betting()

            number = random.randint(1,6)
            win, error = filter_bettings(bot, bettings, number)

            submit_message_channel(bot, win, number)
            submit_message_manager(bot, win, error)
        
        else:

            band = True
