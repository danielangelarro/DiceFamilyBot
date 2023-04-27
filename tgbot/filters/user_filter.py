from telebot.custom_filters import SimpleCustomFilter
from tgbot.models.users_model import Admin
from tgbot.utils.transactions import GAMES


class GameFilter(SimpleCustomFilter):
    """
    Filter games
    """

    key = 'game'
    def check(self, message):

        return message.text in GAMES
