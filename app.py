import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatAction

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TOKEN = '7505260246:AAHmg0mZ3apMvYSQPCIrbnmE7AEvN23xDeo'
ADMIN_IDS = [5387020491]  # Замените на ID вашего аккаунта в Telegram
FILE_PATH = os.path.expanduser('~/xVPN_bot/database/database.db')
BACKUP_PATH = os.path.expanduser('~/xVPN_bot/database/database_backup.db')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    await update.message.reply_text(f'Привет, {user.first_name}!\n'
                                    'Используй /getdb чтобы получить файл базы данных.\n'
                                    'Отправь мне файл database.db чтобы обновить его.')


async def get_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка файла базы данных пользователю"""
    await update.message.chat.send_action(ChatAction.UPLOAD_DOCUMENT)

    try:
        if not os.path.exists(FILE_PATH):
            await update.message.reply_text('Файл базы данных не найден!')
            return

        with open(FILE_PATH, 'rb') as file:
            await update.message.reply_document(
                document=file,
                filename='database.db',
                caption='Текущая база данных'
            )
        logger.info(f"Файл отправлен пользователю {update.effective_user.id}")

    except Exception as e:
        logger.error(f"Ошибка при отправке файла: {e}")
        await update.message.reply_text('⚠️ Произошла ошибка при отправке файла')


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка полученного файла для замены базы данных"""
    user = update.effective_user

    if user.id not in ADMIN_IDS:
        await update.message.reply_text('🚫 У вас нет прав для замены базы данных!')
        return

    document = update.message.document
    if document.file_name != 'database.db':
        await update.message.reply_text('❌ Имя файла должно быть "database.db"')
        return

    await update.message.chat.send_action(ChatAction.UPLOAD_DOCUMENT)

    try:
        # Скачиваем файл
        file = await context.bot.get_file(document.file_id)

        # Создаем резервную копию
        if os.path.exists(FILE_PATH):
            os.replace(FILE_PATH, BACKUP_PATH)

        # Сохраняем новый файл
        await file.download_to_drive(FILE_PATH)

        # Проверяем размер нового файла
        file_size = os.path.getsize(FILE_PATH) / 1024  # в KB
        if file_size < 1:  # Минимальный размер 1KB
            os.replace(BACKUP_PATH, FILE_PATH)  # Восстанавливаем из резервной копии
            raise ValueError("Файл слишком мал, возможно он поврежден")

        await update.message.reply_text(
            f'✅ База данных успешно обновлена!\n'
            f'Размер: {file_size:.2f} KB\n'
            f'Резервная копия сохранена как database_backup.db'
        )
        logger.info(f"База данных обновлена пользователем {user.id}")

    except Exception as e:
        if os.path.exists(BACKUP_PATH):
            os.replace(BACKUP_PATH, FILE_PATH)
        await update.message.reply_text(f'⚠️ Ошибка при обновлении базы данных: {str(e)}')
        logger.error(f"Ошибка при обновлении БД: {e}")


def main() -> None:
    """Запуск бота"""
    # Создаем папку если ее нет
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    # Создаем Application
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getdb", get_db))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Запуск бота
    logger.info("Бот запущен и работает...")
    application.run_polling()


if __name__ == '__main__':
    main()