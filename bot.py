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

COMMANDS = {
    "max": "Знайти максимальне число",
    "min": "Знайти мінімальне число",
}


bot = TeleBot(TELEGRAM_TOKEN)


def is_number(t: str) -> bool:
    return t.lstrip("-").replace(".", "", 1).isdigit()


@bot.message_handler(commands=["max"])
def maximum(message) -> None:
    max_number = None
    numbers = message.text.split()
    for number in numbers:
        if is_number(number):
            if "." in number:
                i = float(number)
            else:
                i = int(number)
            if not max_number:
                max_number = i
            else:
                if i > max_number:
                    max_number = i
    bot.send_message(message.chat.id, str(max_number))


def ping_pong(text: str) -> str:
    if not text.strip().isdigit():
        return text
    n = int(text)
    if (n % 3 == 0) and (n % 5 == 0):
        answer = "Ping Pong"
    elif n % 3 == 0:
        answer = "Ping"
    elif n % 5 == 0:
        answer = "Pong"
    else:
        answer = text
    return answer


@bot.message_handler(content_types=['text'])
def handle_message(message) -> None:
    """
    Обробник текстових повідомлень.

    Функція виконується при отриманні текстового повідомлення від користувача.
    Вона аналізує повідомлення та реагує на нього відповідним чином.

    Параметри:
    - message: Об'єкт, якій містить отримане оновлення від телеграм

    Повертає: None
    """
    print(
        f"{message.from_user.first_name} [{message.chat.id=}]: {message.text}")
    bot.send_message(message.chat.id, ping_pong(message.text))


if __name__ == "__main__":
    print("Встановлюю команди меню...")
    bot.delete_my_commands()
    bot.set_my_commands([BotCommand(k, v) for k, v in COMMANDS.items()])
    print("Слухаю запити...")
    bot.infinity_polling()
