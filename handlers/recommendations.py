from handlers.handler import router
from database import repository 

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.gigachat.gigachat_recomendations import emotion_recommendations

@router.callback_query(lambda c: c.data == "emotion_recommendations")
async def physical_recommendations(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    user_data = await repository.get_user(user_id)
    user_data = user_data[0]

    recommendation = await emotion_recommendations(user_data['age'], user_data['gender'])
    await callback.message.answer(f"{recommendation}", parse_mode="Markdown")
    await callback.answer()

@ButtomRouter.message(lambda message: message.text == "Рекомендации по эмоциональному состоянию")
async def nutrition_recommendations_button(message: Message):
    user_id = message.from_user.id
    user_data = await repository.get_user(user_id)
    user_data = user_data[0]
    recommendation = await emotion_recommendations(user_data['age'], user_data['gender'])

    await message.answer(f"{recommendation}", parse_mode="Markdown")
