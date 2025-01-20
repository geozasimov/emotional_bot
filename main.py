import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.recommendations import ButtomRouter
from handlers import *
from handlers.gigachat.gigachat_mental import quiz_router
from utils import config
from database import repository

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/registration", description="Пройти регистрацию"),
        BotCommand(command="/edit", description="Подкорректируйте данные"),
        BotCommand(command="/profile", description="Ваши данные"),
        BotCommand(command="/report", description="Отчет о вашем состоянии")
    ]
    await bot.set_my_commands(commands)

async def main():
    cfg = config.load()

    telegram_bot = Bot(token=cfg.telegram_token)

    dispatcher = Dispatcher(storage=MemoryStorage())
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    dispatcher.include_router(router)
    dispatcher.include_router(quiz_router)
    dispatcher.include_router(ButtomRouter)
    dispatcher.include_router(gigachat_router)

    dispatcher.update.middleware(UserAuthorizationMiddleware()) 
    dispatcher.update.middleware(UserActionLoggerMiddleware())
    dispatcher.update.middleware(SchedulerMiddleware(scheduler=scheduler))

    await repository.db.connect()

    await set_commands(telegram_bot) 

    print("Бот запущен. Ожидаем сообщений...")
    scheduler.start()

    await dispatcher.start_polling(telegram_bot)

if __name__ == "__main__":
    asyncio.run(main())
