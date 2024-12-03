"""
This module initializes the Telegram bot and sets up the dispatcher for handling updates.

It imports necessary components from the aiogram library and configures logging.
"""
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session import Session
import logging

from app.config import SETTINGS
from .handlers import cmd_router, minion_cmd_router, share_router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# init bots params
session = Session()
storage = MemoryStorage()
bot_init_params = {
    "session": session,
    "storage": storage,
}

# Initialize the Telegram bot (None for the ability to run without a bot token)
main_bot = Bot(SETTINGS.bot_token, **bot_init_params)
# Create a Dispatcher for handling updates
main_dispatcher = Dispatcher()
# Include command routers for handling specific commands
main_dispatcher.include_routers(cmd_router)
main_dispatcher.include_routers(share_router)


minion_dispatcher = Dispatcher()
minion_dispatcher.include_routers(minion_cmd_router)
minion_dispatcher.include_routers(share_router)
