from telebot.custom_filters import SimpleCustomFilter
from tgbot.models.users_model import Admin
from tgbot.utils.bettings import GAMES


class GameFilter(SimpleCustomFilter):
    """
    Filter games
    """

    key = 'game'
    def check(self, message):

        return message.text in GAMES


class AccountFilter(SimpleCustomFilter):
    """
    Filter games
    """

    key = 'account'
    def check(self, message):

        print(message.text, message.text == '**Mi Cuenta**')

        return message.text == '**Mi Cuenta**'