import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Функция для скачивания файла
def download_file(update: Update, context: CallbackContext) -> None:
    file_path = os.path.expanduser("~/BetaTest/database/database.db")  # Путь к файлу

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            context.bot.send_document(chat_id=update.effective_chat.id, document=file)
    else:
        update.message.reply_text('Файл не найден.')


# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Используйте команду /download для скачивания файла.')


# Основная функция
def main() -> None:
    # Вставьте свой токен бота
    TOKEN = "7505260246:AAHmg0mZ3apMvYSQPCIrbnmE7AEvN23xDeo"

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("download", download_file))

    # Запуск бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()