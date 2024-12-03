from urllib.parse import urljoin

from aiogram import Bot
from aiogram.types import Update
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
    url = urljoin(SETTINGS.web_url, MAIN_WEBHOOK_PATH)
    await main_bot.set_webhook(url)
    return {"status": "ok"}


@app.post("/webhook/telegram/main")
async def main_webhook(update: Update):
    result = await main_dispatcher.feed_webhook_update(main_bot, update)
    return StreamingResponse(
        build_response_writer(main_bot, result), media_type="multipart/form-data"
    )


@app.post("/webhook/telegram/{token}")
async def minion_webhook(token: str, update: Update):
    if token not in minion_bots:
        minion_bots[token] = Bot(token=token, **bot_init_params)
    bot = minion_bots[token]
    result = await minion_dispatcher.feed_webhook_update(bot, update)
    return StreamingResponse(
        build_response_writer(bot, result), media_type="multipart/form-data"
    )
