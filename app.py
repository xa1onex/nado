import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await update.message.reply_text('Привет! Используй /getdb чтобы получить файл базы данных.')


async def get_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /getdb для отправки файла базы данных"""
    try:
        # Проверяем существование файла
        if not os.path.exists(FILE_PATH):
            await update.message.reply_text('Файл базы данных не найден!')
            return

        # Отправляем файл
        with open(FILE_PATH, 'rb') as file:
            await update.message.reply_document(
                document=file,
                filename='database.db',
                caption='Вот ваш файл базы данных'
            )
        logger.info("Файл успешно отправлен пользователю %s", update.message.from_user.username)

    except Exception as e:
        logger.error("Ошибка при отправке файла: %s", str(e))
        await update.message.reply_text('Произошла ошибка при отправке файла.')


def main() -> None:
    """Запуск бота"""
    # Создаем Application
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getdb", get_db))

    # Запуск бота
    logger.info("Бот запущен и работает...")
    application.run_polling()


if __name__ == '__main__':
    main()