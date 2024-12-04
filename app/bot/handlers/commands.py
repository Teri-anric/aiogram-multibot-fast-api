from urllib.parse import urljoin

from aiogram import Bot, Router
from aiogram.utils.token import TokenValidationError
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.config import SETTINGS
from app.constant import MINION_WEBHOOK_PATH

cmd_router = Router()


@cmd_router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Hello, create new minion with /add_minion <TOKEN>")


@cmd_router.message(Command("add_minion"))
async def add_minion_command(message: Message, command: CommandObject):
    if not command.args:
        return message.answer("No token provided, usage /add_minion <TOKEN>")
    try:
        minion_bot = Bot(command.args)
        url = urljoin(
            str(SETTINGS.web_url), MINION_WEBHOOK_PATH.format(token=command.args)
        )
        minion_bot.set_webhook(url=url, drop_pending_updates=True)
    except TokenValidationError:
        return message.answer("Invalid token")

    return message.answer("Minion added")
