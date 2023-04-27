from telebot.types import ReplyKeyboardMarkup, KeyboardButton as KB


def reply_main_keyboard():
    markup = ReplyKeyboardMarkup()

    markup.add(KB("🎲 Play"))
    markup.add(KB("📥 Deposito"), KB("🏧 Balance"), KB("📤 Retiro"))
    markup.add(KB("👨‍💻 Soporte"))
    markup.add(KB("📝 Terminos y Condiciones"))

    return markup
