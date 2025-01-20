import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers.commands import register_handlers
from db.database import init_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

# Регистрация команд
async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="motivate", description="Получить мотивацию"),
        BotCommand(command="emotion", description="Узнать описание эмоции"),
        BotCommand(command="add_emotion", description="Добавить новую эмоцию"),
    ]
    await bot.set_my_commands(commands)

# Инициализация
async def main():
    logging.info("Запуск бота...")
    await init_db()  # Создание базы данных, если её нет
    register_handlers(dp)  # Регистрация обработчиков
    await set_bot_commands()  # Установка команд
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
