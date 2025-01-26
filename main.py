import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from handlers.recommendations import ButtonRouter
from handlers import *
from utils import config
from database import repository

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/registration", description="Пройти регистрацию"),
        BotCommand(command="/edit", description="Подкорректируйте данные"),
        BotCommand(command="/profile", description="Ваши данные")
    ]
    await bot.set_my_commands(commands)

async def main():
    cfg = config.load()

    telegram_bot = Bot(token=cfg.telegram_token)
    
    # Ensure the client session is closed properly
    async with telegram_bot:
        dispatcher = Dispatcher(storage=MemoryStorage())

        # Include routers (make sure 'router' is defined)
        dispatcher.include_router(router)
        dispatcher.include_router(ButtonRouter)
        dispatcher.include_router(gigachat_router)

        # Middleware Initialization
        dispatcher.update.middleware(UserAuthorizationMiddleware()) 
        dispatcher.update.middleware(UserActionLoggerMiddleware())

        await repository.db.connect()  # Make sure db connection is handled

        await set_commands(telegram_bot) 

        print("Бот запущен. Ожидаем сообщений...")

        await dispatcher.start_polling(telegram_bot)

if name == "main":
    asyncio.run(main())
