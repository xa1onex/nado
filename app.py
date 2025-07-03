import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего Telegram бота
TOKEN = '7505260246:AAHmg0mZ3apMvYSQPCIrbnmE7AEvN23xDeo'

# Путь к файлу на сервере
FILE_PATH = os.path.expanduser('~/BetaTest/database/database.db')


def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    update.message.reply_text('Привет! Используй /getdb чтобы получить файл базы данных.')


def get_db(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /getdb для отправки файла базы данных"""
    try:
        # Проверяем существование файла
        if not os.path.exists(FILE_PATH):
            update.message.reply_text('Файл базы данных не найден!')
            return

        # Отправляем файл
        with open(FILE_PATH, 'rb') as file:
            update.message.reply_document(
                document=file,
                filename='database.db',
                caption='Вот ваш файл базы данных'
            )
        logger.info("Файл успешно отправлен пользователю %s", update.message.from_user.username)

    except Exception as e:
        logger.error("Ошибка при отправке файла: %s", str(e))
        update.message.reply_text('Произошла ошибка при отправке файла.')


def main() -> None:
    """Запуск бота"""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("getdb", get_db))

    # Запуск бота
    updater.start_polling()
    logger.info("Бот запущен и работает...")
    updater.idle()


if __name__ == '__main__':
    main()