from handlers.handler import router
from database import repository

from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

class EditProfile(StatesGroup):
    age = State()
    height = State()
    weight = State()

edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить возраст", callback_data="edit_age"),
        ],
    ]
)

@router.message(Command('profile'))
async def show_profile(message: Message):
    user_id = message.from_user.id

    user_data = await repository.get_user(user_id)
    user_data = user_data[0]

    profile_text = (
        f"Ваш профиль:\n"
        f"Имя: {user_data['name'] or 'Не указано'}\n"
        f"Возраст: {user_data['age'] or 'Не указано'}\n"
        f"Пол: {user_data['gender'] or 'Не указано'}\n"
        f"Если хотите изменить данные, напишите команду /edit и выберите, что изменить."
    )

    await message.answer(profile_text)


@router.message(Command('edit'))
async def edit_profile(message: Message):
    await message.answer("Выберите, что вы хотите изменить:", reply_markup=edit_keyboard)

@router.callback_query(lambda c: c.data == "edit_age")
async def edit_age(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите новый возраст:")
    await state.set_state(EditProfile.age)
    await callback.answer()

@router.message(EditProfile.age)
async def update_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer("Пожалуйста, введите корректный возраст (число).")
        return

    new_age = int(message.text)
    user_id = message.from_user.id

    await repository.update_parameter(user_id, "age", new_age)

    await message.answer("Ваш возраст успешно обновлён.")
    await state.clear()

