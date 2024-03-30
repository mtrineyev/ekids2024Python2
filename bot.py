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
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    print("Бот слухає запити...")
    bot.infinity_polling()
