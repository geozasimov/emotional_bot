from handlers.registration import Registration
from database import repository

from aiogram.types import Update
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

class UserAuthorizationMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        
        state = data.get('raw_state', None)

        # Проверяем строковое состояние вместо объекта
        if state and state in [
            str(Registration.name),
            str(Registration.age),
            str(Registration.gender)
        ]:
            return await handler(event, data)

        user_id = None

        if event.message:
            user_id = event.message.from_user.id
        elif event.callback_query:
            user_id = event.callback_query.from_user.id

        if not user_id:
            return await handler(event, data)
        
        user = await repository.get_user(user_id)
        
        if not user and event.message and event.message.text:
            if not event.message.text.startswith('/registration') and not event.message.text.startswith('/start'):
                await event.message.answer("Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь, чтобы использовать бота.")
                return
    
        return await handler(event, data)
