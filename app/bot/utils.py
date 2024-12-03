"""
Utility functions for Telegram bot webhook response handling.

This module provides utility functions to build multipart responses
for Telegram bot webhook updates, with support for various data types
and file attachments.
"""

import secrets
from typing import Dict, Optional

from aiogram import Bot
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType
from aiogram.types import InputFile
from aiohttp import MultipartWriter


def build_response_writer(
    bot: Bot, result: Optional[TelegramMethod[TelegramType]]
) -> MultipartWriter:
    """
    Build a MultipartWriter for sending a response to a Telegram webhook.

    Args:
        bot (Bot): The instance of the Bot to use for handled requests.
        result (Optional[TelegramMethod[TelegramType]]): The result of a Telegram method call.

    Returns:
        MultipartWriter: A writer for the multipart/form-data request.
    """
    # Create a MultipartWriter with a unique boundary to separate form data parts
    writer = MultipartWriter(
        "form-data",
        boundary=f"webhookBoundary{secrets.token_urlsafe(16)}",
    )
    
    # If no result is provided, return an empty writer
    if not result:
        return writer

    # Append the API method name to the writer
    payload = writer.append(result.__api_method__)
    payload.set_content_disposition("form-data", name="method")

    # Prepare a dictionary to store file attachments
    files: Dict[str, InputFile] = {}
    
    # Iterate through all result attributes and prepare their values
    for key, value in result.model_dump(warnings=False).items():
        # Prepare the value, converting it to a format suitable for sending
        value = bot.session.prepare_value(value, bot=bot, files=files)
        if not value:
            continue
        
        # Append each non-file value to the writer
        payload = writer.append(value)
        payload.set_content_disposition("form-data", name=key)

    # Append any file attachments to the writer
    for key, value in files.items():
        payload = writer.append(value.read(bot))
        payload.set_content_disposition(
            "form-data",
            name=key,
            filename=value.filename or key,
        )

    return writer