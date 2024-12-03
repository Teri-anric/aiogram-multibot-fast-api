"""
Share logic between main and minion bots

You can convert this module to a package in the future
"""

from aiogram import Router
from aiogram.types import Message

share_router = Router()


@share_router.message()
async def echo_message(message: Message):
    await message.answer(message.text)
