from aiogram import BaseMiddleware
from aiogram.types import Message
from data.queries import save_user
from typing import Callable, Dict, Any, Awaitable


class SaveUserMiddleware(BaseMiddleware):
    """ Миддлварь сохраняет / пытается сохранить пользователя после вызова любой команды """
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        save_user(event.from_user.id)
        return await handler(event, data)