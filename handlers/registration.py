from handlers.handler import router
from database import repository
from handlers import daily_survey
from handlers import review

from aiogram import Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
from zoneinfo import ZoneInfo 

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

class Registration(StatesGroup):
    name = State()
    age = State()
    gender = State()
    
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
    if not message.text.isalpha():
        await message.answer("Пожалуйста, введите имя буквами.")
        return
    if len(message.text) > 20:
        await message.answer("Имя слишком длинное.")
        return

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
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мужской', callback_data='gender_m')],
        [InlineKeyboardButton(text='Женский', callback_data='gender_f')]
    ])
    await message.answer('Выберите ваш пол:', reply_markup=keyboard)

@router.callback_query()
async def add_gender(callback: CallbackQuery, state: FSMContext):
    gender = callback.data.split('_')[1]
    await callback.message.edit_reply_markup(reply_markup=None)
    
    await state.update_data(gender=gender)
    data = await state.get_data()
    await state.clear()

    await repository.add_user(
        user_id=callback.from_user.id,
        name=data.get("name"),
        age=int(data.get("age")),
        gender=data.get("gender"),
    )

    await callback.message.answer(f"Приятно познакомиться, {data.get('name')}!")
