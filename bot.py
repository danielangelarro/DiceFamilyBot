# callbacks
from tgbot.callbacks.callback_games import select_game_callback
from tgbot.callbacks.callback_games import dice_callback, tall_and_bass_callback
from tgbot.callbacks.callback_games import dbomb_callback
from tgbot.callbacks.callback_deposite import autorized_deposite_callback, cancel_deposite_callback
from tgbot.callbacks.callback_retire import autorized_retire_callback, cancel_retire_callback

# filters
from tgbot.filters.admin_filter import AdminFilter

# handlers
from tgbot.handlers.admin import admin_user, groups_info_admin, info_messaje_by_admin
from tgbot.handlers.spam_command import wrap_group
from tgbot.handlers.user import any_user, my_account, betting, deposite_cash, handle_photo, support, termine_and_conditions
from tgbot.handlers.retire import retire_cash

# middlewares
from tgbot.middlewares.antiflood_middleware import antispam_func

# states
from tgbot.states.register_state import Register

# utils
from tgbot.utils.database import DBManager
from tgbot.utils.subprocess import async_game

# telebot
from telebot import TeleBot
from telebot.types import BotCommand, BotCommandScopeAllPrivateChats

# config
from tgbot import config

db = DBManager(config.DATABASE)

# middlewares:
from telebot import apihelper
apihelper.ENABLE_MIDDLEWARE = True

# I recommend increasing num_threads
bot = TeleBot(config.TOKEN, num_threads=5)

# pool threading for the logic game
import threading
game_thread = threading.Thread(target=async_game, args=(bot,))

def register_handlers():
    bot.register_message_handler(admin_user, commands=['start'], admin=True, pass_bot=True, chat_types=['private'])
    bot.register_message_handler(any_user, commands=['start'], admin=False, pass_bot=True, chat_types=['private'])
    bot.register_message_handler(groups_info_admin, commands=['group'], admin=True, pass_bot=True)
    bot.register_message_handler(wrap_group, commands=['get_info'], pass_bot=True)
    bot.register_message_handler(handle_photo, content_types=['photo'], pass_bot=True)
    # bot.register_message_handler(info_messaje_by_admin, admin=True, pass_bot=True)
    
    bot.register_message_handler(betting,  func=lambda m: m.text=='🎲 Play', pass_bot=True, chat_types=['private'])
    bot.register_message_handler(deposite_cash,  func=lambda m: m.text=='📥 Deposito', pass_bot=True, chat_types=['private'])
    bot.register_message_handler(my_account, func=lambda m: m.text=='🏧 Balance', pass_bot=True)
    bot.register_message_handler(retire_cash,  func=lambda m: m.text=='📤 Retiro', pass_bot=True, chat_types=['private'])
    
    bot.register_message_handler(support, func=lambda m: m.text=='👨‍💻 Soporte', pass_bot=True)
    bot.register_message_handler(termine_and_conditions, func=lambda m: m.text=='📝 Terminos y Condiciones', pass_bot=True, chat_types=['private'])

def register_callbacks():
    bot.register_callback_query_handler(select_game_callback, func=lambda c: c.data[:6]=='games-', pass_bot=True)
    bot.register_callback_query_handler(dice_callback, func=lambda c: c.data[:5]=='dice-', pass_bot=True)
    bot.register_callback_query_handler(tall_and_bass_callback, func=lambda c: c.data[:3]=='tb-', pass_bot=True)
    bot.register_callback_query_handler(dbomb_callback, func=lambda c: c.data[:6]=='dbomb-', pass_bot=True)
    bot.register_callback_query_handler(autorized_deposite_callback, func=lambda c: c.data=='deposite-validate', pass_bot=True)
    bot.register_callback_query_handler(cancel_deposite_callback, func=lambda c: c.data=='deposite-cancel', pass_bot=True)
    bot.register_callback_query_handler(autorized_retire_callback, func=lambda c: c.data=='retire-validate', pass_bot=True)
    bot.register_callback_query_handler(cancel_retire_callback, func=lambda c: c.data=='retire-cancel', pass_bot=True)

def register_commands():
    bot.delete_my_commands(scope=None, language_code=None)

    bot.set_my_commands(
        commands=[
            BotCommand("start", "Inicia el bot")
        ],
        # scope=telebot.types.BotCommandScopeChat(12345678)  # use for personal command for users
        scope = BotCommandScopeAllPrivateChats()  # use for all private chats
    )

register_handlers()
register_callbacks()
register_commands()

print('Register success...')

# Middlewares
bot.register_middleware_handler(antispam_func, update_types=['message'])


# custom filters
bot.add_custom_filter(AdminFilter())

def run():

    game_thread.start()
    bot.infinity_polling()


run()
