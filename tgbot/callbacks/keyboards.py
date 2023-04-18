from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.utils.transactions import GAMES


def games_keyboard():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text = game,
                    callback_data = f'games-{game}'
                )
            ]
            for game in GAMES
        ]
    )


def dice_keyboard():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text = str(number),
                    callback_data = f'dice-{number}'
                )
                for number in range(1, 7)
            ],
            [
                InlineKeyboardButton(
                    text = 'Cancelar',
                    callback_data = 'cancel-betting'
                )
            ]
        ]
    )


def tall_and_bass_keyboard():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text = 'TALL',
                    callback_data = 'tb-tall'
                ),
                InlineKeyboardButton(
                    text = 'BASS',
                    callback_data = 'tb-bass'
                )
            ],
            [
                InlineKeyboardButton(
                    text = 'Cancelar',
                    callback_data = 'cancel-betting'
                )
            ]
        ]
    )


def dbomb_keyboard():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text = str(number),
                    callback_data = f'dbomb-{number}'
                )
                for number in range(1, 7)
            ],
            [
                InlineKeyboardButton(
                    text = 'Cancelar',
                    callback_data = 'cancel-betting'
                )
            ]
        ]
    )


def validate_keyboard():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text = '✅ Validar',
                    callback_data = f'betting-validate'
                )
            ]
        ]
    )

def validate_deposite_keyboard():
    return InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(
                    text = '✅ Validar',
                    callback_data = f'deposite-validate'
                ),
                InlineKeyboardButton(
                    text = '❌ Rechazar',
                    callback_data = f'deposite-cancel'
                )
            ]
        ]
    )