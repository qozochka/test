""" Модуль подсказок для команд бота """

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    """Устанавливает подсказки для команд бота"""

    commands = [
        BotCommand(
            command="/start",
            description="Начало работы с ботом"),
        BotCommand(
            command="/help",
            description="Помощь в работе с ботом",
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())