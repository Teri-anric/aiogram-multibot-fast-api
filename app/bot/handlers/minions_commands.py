from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

minion_cmd_router = Router()


@minion_cmd_router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Hello, world!")
