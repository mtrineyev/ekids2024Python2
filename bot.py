"""
Bot.py - Основний скрипт для телеграм-бота.

Цей скрипт містить логіку для запуску та функціональність телеграм-бота.
Він використовує різноманітні модулі та функції для обробки повідомлень,
реагування на події, взаємодії з базою даних
та надання відповідей користувачам.

Автор: Максим Трінеєв

"""


from telebot import TeleBot
from components.settings import TELEGRAM_TOKEN


bot = TeleBot(TELEGRAM_TOKEN)


def ping_pong(text: str) -> str:
    if not text.isdigit():
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
    print("Бот слухає запити...")
    bot.infinity_polling()
