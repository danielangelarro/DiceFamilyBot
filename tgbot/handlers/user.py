from telebot import TeleBot
from telebot.types import Message

import tgbot.config as config
from tgbot.callbacks.keyboards import games_keyboard, validate_deposite_keyboard
from tgbot.callbacks.reply_keyboard import reply_main_keyboard
from tgbot.utils.transactions import register_user, get_money, send_deposite


def any_user(message: Message, bot: TeleBot):
    """
    Users messages handlers.
    """

    register_user(message.from_user)

    text =  f'¡Bienvenido @{message.from_user.username} al Bot del Proyecto Dice! 🎲\n\n' \
            '😁¡Apostemos y divirtámonos!\n\n' \
            'Selecciona uno de nuestros tres juegos:\n' \
            '🎲 Dice Classic: adivina el número del dado.\n\n' \
            '📈 Tall & Bass: predice si el número será alto o bajo.\n\n' \
            '💣 DBomb: elige el dado que no saldrá.\n\n\n' \
            '¡Buena suerte!🍀'

    bot.send_message(message.chat.id, text=text, reply_markup=reply_main_keyboard())


def betting(message: Message, bot: TeleBot):

    chat_id = message.chat.id

    bot.send_dice(chat_id=chat_id, emoji='🎰')
    bot.send_message(chat_id=chat_id, text='**Selecciona un modo de juego**', reply_markup=games_keyboard(), parse_mode='MarkdownV2')


def my_account(message: Message, bot: TeleBot):

    chat_id = message.chat.id
    money = get_money(chat_id)

    sticker_id = 'CAACAgIAAxkBAAICcmRJxwz3TrpU92O88R9FT8l7jMNDAAIFAAMWbkwS9hEQhS3h0QwvBA'
    text =  '🎉 ¡Felicidades!\n\n' \
            f'Tu balance actual es de 💰 {money} 💰.\n' \
            '¡Sigue apostando y ganando! 💸💰🤑\n\n' \
            'No olvides apostar responsablemente. 🎲🃏✨\n\n' \
            '¡Que tengas un buen día! 😊'

    bot.send_sticker(chat_id, sticker_id)
    bot.send_message(chat_id, text)


def deposite_cash(message: Message, bot: TeleBot):

    chat_id = message.chat.id
    text = 'Envie una captura 🖼 de su transferencia y en la descripcion de la imagen coloque la cantidad a depositar.\n' \
            f'\n💳 Tarjeta a depositar: {config.TARJECT_CUP}'

    bot.send_message(chat_id=chat_id, text=text)


def support(message: Message, bot: TeleBot):

    chat_id = message.chat.id
    text = 'Redacte un breve ensaje explicando su situacion a los administradores:'

    bot.send_message(chat_id=chat_id, text=text)
    bot.register_next_step_handler(message, support_step, bot)


def termine_and_conditions(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    text = '''Términos y Condiciones

Los presentes términos y condiciones rigen el uso y la participación en el juego de casino de dados de Telegram (el “Juego”). Estos términos y condiciones son acuerdos legales entre usted (el “Usuario”) y los creadores del Juego (el “Organizador”).

Al participar en el Juego, el Usuario acepta cumplir con los términos y condiciones aquí establecidos. El Organizador se reserva el derecho a cambiar estos términos y condiciones en cualquier momento sin previo aviso.

1. Seguridad de los datos

El Organizador se compromete a garantizar la seguridad de los datos de sus usuarios. Esto incluye su información personal y financiera. Esta información se gestiona en un entorno seguro y está protegida por un firewall adecuado.

2. Transacciones seguras

El Organizador se compromete a proporcionar transacciones seguras para que los usuarios realicen sus pagos. Cada una de estas transacciones se realiza por medio de una plataforma certificada para evitar el fraude.

3. Cumplimiento de la ley

El Organizador se compromete a cumplir con la legislación y regulaciones aplicables y apropiadas.

4. Protección y uso justo de los datos personales

El Organizador se compromete a proteger los datos personales de sus usuarios y a garantizar que estos serán únicamente utilizados para los fines para los cuáles fueron recopilados.

5. Protección de los usuarios

El Organizador se compromete a proteger a sus usuarios de la manipulación basada en la corrupción. El Organizador no tolerará el uso de programas no autorizados o la manipulación de los resultados del Juego con algún tipo de finalidad fraudulenta.

6. Limitación de responsabilidad

El Organizador se compromete a cubrir cualquier responsabilidad resultante de la falla en conducción del Juego, como el uso indebido de los sistemas informáticos, la corrupción de los resultados del Juego, el fraude de parte de los usuarios, etc.

7. Fraude

El Organizador se reserva el derecho de tomar acciones legales contra los usuarios que hayan cometido, sean acusados ​​de haber cometido, o sean sospechosos de haber cometido actividades fraudulentas, como el comportamiento abusivo, la manipulación de los resultados del Juego, la violación de las leyes locales, la falta de respeto a la moralidad o el bienestar general de los demás usuarios, etc.

8. Discreción

El Organizador se compromete a garantizar que todos los datos de los usuarios sean tratados con la máxima discreción.
    '''

    bot.send_message(chat_id=chat_id, text=text)


def support_step(message: Message, bot: TeleBot):
    
    text = f'💬 **MENSAJE A SOPORTE** 💬\n\n👤: @{message.from_user.username}\n\n\"{message.text}\"'

    bot.send_message(config.CHANNEL_PRIVATE_URL, text)
    bot.send_message(message.chat.id, 'Su mensje se ha enviado correctamente a los administradores.')


def handle_photo(message: Message, bot: TeleBot):
    
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        photo_id = message.photo[-1].file_id
        money = message.caption

        caption = '\n\n' \
                f'👤 Usuario: @{message.from_user.username}\n' \
                f'🪪 Nombre: {message.from_user.full_name}\n' \
                f'💰 Dinero: {money}\n'

        bot.send_message(chat_id, f"FORMULARIO DE DEPÓSITO. {caption}")
        msg = bot.send_photo(chat_id=config.CHANNEL_PRIVATE_URL, photo=photo_id, caption=caption, 
                    reply_markup=validate_deposite_keyboard())
        
        send_deposite(msg.message_id, float(money), user_id)
    
    except Exception as e:
        
        chat_id = message.chat.id

        print(e)

        bot.delete_message(chat_id, message.message_id)
        bot.send_message(chat_id, '⛔ Mensaje inválido. Vuelva a intentarlo.')
