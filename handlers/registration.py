from handlers.handler import router
from database import repository
from handlers import daily_survey
from handlers import review

from aiogram import Router
from aiogram import Bot
from aiogram import types
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from zoneinfo import ZoneInfo 

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

router = Router()

class Registration(StatesGroup):
    name = State()
    age = State()
    gender = State()

recommendation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рекомендации по эмоциональному состоянию", callback_data="emotion_recommendations")],
        
    ]
)

@router.message(Command('registration'))
async def start_registration(message: Message, state: FSMContext):
    user = await repository.get_user(message.from_user.id)
    if user:
        await message.answer('Вы уже зарегистрированы.')
        return
    await state.set_state(Registration.name)
    await message.answer('Введите ваше имя:')

@router.message(Registration.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.age)
    await message.answer('Введите ваш возраст:')

@router.message(Registration.age)
async def add_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer("Пожалуйста, введите корректный возраст (число).")
        return
    await state.update_data(age=message.text)
    await state.set_state(Registration.gender)
    await message.answer('Введите ваш пол(м/ж):')

@router.message(Registration.gender)
async def add_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    await message.answer(f"Вы указали пол: {data['gender']}")
    
@router.message(Registration.gender)
async def add_gender(message: types.Message, state: FSMContext):
    if message.text.lower() != "м" and message.text.lower() != "ж":
        await message.answer("Пожалуйста, введите свой пол корректно(м/ж)")
        return
    data = await state.get_data()
    await message.answer(f"Вы указали пол: {data['gender']}")
    await repository.add_user(
        user_id = message.from_user.id,
        name=data.get("name"),
        age=int(data.get("age")),
        gender=data.get("gender")
    )

    await callback.message.answer(f"Приятно познакомиться, {data.get('name')}!\nТеперь каждый день вечером вам будет предложено пройти анкетирование для отслеживание вашего состояния.\nКаждую неделю вы сможете смотреть отчет и получать мою рецензию!")
   

