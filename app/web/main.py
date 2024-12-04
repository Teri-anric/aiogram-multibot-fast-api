"""
Web module for handling Telegram bot webhooks.

This module sets up FastAPI endpoints for processing webhook updates
for both the main bot and dynamically created minion bots.
It provides webhook setup and update processing functionality.
"""

from urllib.parse import urljoin

from aiogram import Bot
from aiogram.types import Update
from aiogram.methods import TelegramMethod
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.bot import (bot_init_params, main_bot, main_dispatcher,
                     minion_dispatcher)
from app.bot.utils import build_response_writer
from app.config import SETTINGS
from app.constant import MAIN_WEBHOOK_PATH

app = FastAPI()
# cache bot obj
minion_bots = {}


@app.get("/webhook/telegram/main")
async def main_webhook():
    """
    Set up the webhook for the main Telegram bot.
    
    This endpoint configures the webhook URL for the main bot,
    allowing Telegram to send updates to this specific endpoint.
    
    Returns:
        dict: A status confirmation that the webhook was set up successfully.
    """
    url = urljoin(str(SETTINGS.web_url), MAIN_WEBHOOK_PATH)
    await main_bot.set_webhook(url, drop_pending_updates=True)
    return {"status": "ok"}


@app.post("/webhook/telegram/main")
async def main_webhook(update: Update):
    """
    Process incoming webhook updates for the main Telegram bot.
    
    This endpoint receives updates from Telegram for the main bot,
    feeds the update to the dispatcher, and streams the response.
    
    Args:
        update (Update): The incoming Telegram update object.
    
    Returns:
        StreamingResponse: A streaming response containing the bot's reaction to the update.
    """
    result = await main_dispatcher.feed_webhook_update(main_bot, update)
    if isinstance(result, TelegramMethod):
        await main_dispatcher.silent_call_request(main_bot, result)
    return StreamingResponse(None, status_code=200)


@app.post("/webhook/telegram/{token}")
async def minion_webhook(token: str, update: Update):
    """
    Process incoming webhook updates for dynamically created Telegram bots.
    
    This endpoint handles updates for multiple bot instances identified by their unique token.
    If a bot with the given token doesn't exist, it is dynamically created.
    
    Args:
        token (str): The unique bot token used to identify and initialize the bot.
        update (Update): The incoming Telegram update object.
    
    Returns:
        StreamingResponse: A streaming response containing the bot's reaction to the update.
    """
    if token not in minion_bots:
        minion_bots[token] = Bot(token=token, **bot_init_params)
    bot = minion_bots[token]
    result = await minion_dispatcher.feed_webhook_update(bot, update)
    if isinstance(result, TelegramMethod):
        await minion_dispatcher.silent_call_request(bot, result)
    return StreamingResponse(None, status_code=200)