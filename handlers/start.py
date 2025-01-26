from handlers.handler import router
from database import repository

from aiogram import types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

user_states = {}



main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Информация о команде"), KeyboardButton(text="Эмоция")],
        [KeyboardButton(text="Мотивация"), KeyboardButton(text="Совет")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@router.message(CommandStart())
async def start(message: Message):
    user = await repository.get_user(message.from_user.id)
    if user:
        user_name = user[0]['name']
    else:
        user_name = message.from_user.first_name
    
    await message.answer(
        f"Привет, {user_name}!\nЯ помогу тебе развить эмоциональнный интеллект. Вот, что я могу:\n - Сгенерировать совет для развития твоего эмоционального интеллекта \n - Описать тебе какую-нибудь эмоцию \n - Не хватает мотивации?  \n Но сначала зарегистрируйся, чтобы использовать весь мой функционал -> /registration",
        reply_markup = main_keyboard
    )

@router.message(lambda message: message.text == "Информация о команде")
async def handle_project_info(message: types.Message):
    await message.answer(
        "Информация о команде:\n"
        "Этот бот создан для развития эмоционального интеллекта.\n"
        "Проект выполнен в рамках научно-исследовательского семинара"
        '"Искусственный интеллект в инженерном образовании"'
        "МИЭМ НИУ ВШЭ студентами группы БИВ234:\n"
        "- Чибировым Русланом\n"
        "- Засимовым Георгием."
    )


@router.message(lambda message: message.text == "Поддержка")
async def handle_support(message: types.Message):
    await message.answer(
        "Свяжитесь с разработчиком:\n"
        "[Написать в Telegram (1)](https://t.me/chib_rus)\n",
        parse_mode="Markdown"
    )



