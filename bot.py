"""
Bot.py - Основний скрипт для телеграм-бота.

Цей скрипт містить логіку для запуску та функціональність телеграм-бота.
Він використовує різноманітні модулі та функції для обробки повідомлень,
реагування на події, взаємодії з базою даних
та надання відповідей користувачам.

Автор: Максим Трінеєв

"""

from telebot import TeleBot
from telebot.types import BotCommand
from components.settings import TELEGRAM_TOKEN
from random import choice, randint
from urllib.parse import quote_plus

COMMANDS = {
    "dice": "Гральний кубик",
    "hello": "Привітатися",
    "max": "Знайти максимальне число",
    "min": "Знайти мінімальне число",
    "pingpong": "Міні гра 'Пінг Понг'",
    "qr": "Створити QR-код",
    "bet": "Зробити ставку на червоне або чорне",
}
GREETINGS = (
    "Hello",
    "Привіт",
    "Вітаю",
    "Aloha",
    "Здоровенькі були",
)
DICE_NUMBERS = ("0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣")
BETS = [
    ["🟥", "червоне", "red"],
    ["⬛️", "чорне", "black"],
]

# QR Api documentation: https://goqr.me/api/doc/create-qr-code/
QR_SIZE = 200
QR_API = \
    "https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={data}"


bot = TeleBot(TELEGRAM_TOKEN)


def is_number(t: str) -> bool:
    return t.lstrip("-").replace(".", "", 1).isdigit()


def is_natural(t: str) -> bool:
    try:
        n = int(t)
    except ValueError:
        return False
    return n >= 0


def number(t: str) -> [int | float]:
    if "." in t:
        return float(t)
    else:
        return int(t)


@bot.message_handler(commands=["max"])
def maximum(message) -> None:
    max_number = None
    elements = message.text.split()
    for element in elements:
        if is_number(element):
            x = number(element)
            if not max_number:
                max_number = x
            elif x > max_number:
                max_number = x
    bot.send_message(message.chat.id, str(max_number))


@bot.message_handler(commands=["min"])
def minimum(message) -> None:
    min_number = None
    elements = message.text.split()
    for element in elements:
        if is_number(element):
            x = number(element)
            if not min_number:
                min_number = x
            elif x < min_number:
                min_number = x
    bot.send_message(message.chat.id, str(min_number))


@bot.message_handler(commands=["pingpong"])
def ping_pong(message) -> None:
    parameter = message.text[len("/pingpong "):]
    if not is_natural(parameter):
        bot.send_message(message.chat.id, "Не натуральне число")
        return
    n = number(parameter)
    if n % 3 == 0 and n % 5 == 0:
        response = "Ping Pong"
    elif n % 3 == 0:
        response = "Ping"
    elif n % 5 == 0:
        response = "Pong"
    else:
        response = parameter
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=["hello"])
def hello(message) -> None:
    bot.send_message(message.chat.id, choice(GREETINGS))


@bot.message_handler(commands=["dice"])
def dice(message) -> None:
    bot.send_message(message.chat.id, DICE_NUMBERS[randint(1, 6)])


@bot.message_handler(commands=["qr"])
def qr_generator(message) -> None:
    qr_data = message.text[len("/qr "):]
    if not qr_data:
        bot.send_message(message.chat.id, "Потрібен параметр")
        return
    bot.send_photo(
        message.chat.id,
        # open("img.png", "rb"),
        QR_API.format(size=QR_SIZE, data=quote_plus(qr_data)),
        caption=qr_data
    )


@bot.message_handler(commands=["bet"])
def make_bet(message) -> None:
    user_bet = message.text[len("/bet "):].lower()
    if not any([user_bet in b for b in BETS]):
        bot.send_message(
            message.chat.id, "Ставка повинна бути на червоне або чорне")
        return
    bot_bet = choice(BETS)
    bot.send_message(
        message.chat.id, bot_bet[0])
    if user_bet in bot_bet:
        bot.send_message(
            message.chat.id, "Ви перемогли!")
    else:
        bot.send_message(
            message.chat.id, "Ви програли")


def listener(messages):
    for m in messages:
        if m.content_type == "text":
            print(f"{m.from_user.first_name} [{m.chat.id=}]: {m.text}")


@bot.message_handler(content_types=["text"])
def handle_message(message) -> None:
    """
    Обробник текстових повідомлень.

    Функція виконується при отриманні текстового повідомлення від користувача.
    Вона аналізує повідомлення та реагує на нього відповідним чином.

    Параметри:
    - message: Об'єкт, якій містить отримане оновлення від телеграм

    Повертає: None
    """
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    print("Встановлюю команди меню...")
    bot.delete_my_commands()
    bot.set_my_commands([BotCommand(k, v) for k, v in COMMANDS.items()])
    bot.set_update_listener(listener)
    print("Слухаю запити...")
    bot.infinity_polling()
