from handlers.handler import router
from database import repository

from aiogram import Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
import asyncio

from datetime import datetime

class SurveyStates(StatesGroup):
    physical_activity = State()
    stress_level = State()
    mood_level = State()
    sleep_quality = State()
    additional_notes = State()


async def send_daily_survey(user_id, bot: Bot, state: FSMContext):
    interval = 30 

    while True:
        current_state = await state.get_state()
        
        if current_state is None:
            await bot.send_message(user_id, "Привет! Пора пройти ежедневное анкетирование.")
            
            buttons = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Вообще нет эмоционального состояния", callback_data="0:Нет")],
                    [InlineKeyboardButton(text="Лёгкое эмоциональное состояние", callback_data="1:Легкое")],
                    [InlineKeyboardButton(text="Умеренное эмоциональное состояние", callback_data="2:Умеренное")],
                    [InlineKeyboardButton(text="Высокое эмоциональное состояние", callback_data="3:Высокое")],
                ]
            )
            await bot.send_message(user_id, "Какой у вас уровень эмоционального состояния сегодня?", reply_markup=buttons)

            await state.set_state(SurveyStates.physical_activity)
            return 

        await asyncio.sleep(interval) 
        
@router.callback_query(SurveyStates.physical_activity)
async def survey_physical_activity(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    await state.update_data(physical_activity=answer)
    await callback.message.edit_text("Уровень стресса сегодня?")

    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Очень низкий", callback_data="1:Очень низкий")],
            [InlineKeyboardButton(text="Низкий", callback_data="2:Низкий")],
            [InlineKeyboardButton(text="Средний", callback_data="3:Средний")],
            [InlineKeyboardButton(text="Высокий", callback_data="4:Высокий")],
            [InlineKeyboardButton(text="Очень высокий", callback_data="5:Очень высокий")],
        ]
    )
    await callback.message.edit_reply_markup(reply_markup=buttons)
    await state.set_state(SurveyStates.stress_level)

@router.callback_query(SurveyStates.stress_level)
async def survey_stress_level(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    await state.update_data(stress=answer)
    await callback.message.edit_text("Как вы оцениваете своё настроение сегодня?")

    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Очень плохое", callback_data="1:Очень плохое")],
            [InlineKeyboardButton(text="Плохое", callback_data="2:Плохое")],
            [InlineKeyboardButton(text="Среднее", callback_data="3:Среднее")],
            [InlineKeyboardButton(text="Хорошее", callback_data="4:Хорошее")],
            [InlineKeyboardButton(text="Очень хорошее", callback_data="5:Очень хорошее")],
        ]
    )
    await callback.message.edit_reply_markup(reply_markup=buttons)
    await state.set_state(SurveyStates.mood_level)

@router.callback_query(SurveyStates.mood_level)
async def survey_mood_level(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    await state.update_data(mood=answer)
    await callback.message.edit_text("Как вы оцените качество вашего сна сегодня?")

    buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Очень плохое", callback_data="1:Очень плохое")],
            [InlineKeyboardButton(text="Плохое", callback_data="2:Плохое")],
            [InlineKeyboardButton(text="Среднее", callback_data="3:Среднее")],
            [InlineKeyboardButton(text="Хорошее", callback_data="4:Хорошее")],
            [InlineKeyboardButton(text="Очень хорошее", callback_data="5:Очень хорошее")],
        ]
    )
    await callback.message.edit_reply_markup(reply_markup=buttons)
    await state.set_state(SurveyStates.sleep_quality)

@router.callback_query(SurveyStates.sleep_quality)
async def survey_sleep_quality(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    await state.update_data(sleep_quality=answer)

    data = await state.get_data()
    data['survey_date'] = datetime.now()
    user_id = callback.from_user.id 
    await repository.save_survey_data(user_id, data)

    await callback.message.edit_text("Спасибо за участие в анкетировании! Ваши ответы были сохранены.")
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.clear()
