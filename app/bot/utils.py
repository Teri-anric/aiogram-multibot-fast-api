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

def build_multipart_response(
    bot: Bot, result: Optional[TelegramMethod[TelegramType]]
) -> MultipartWriter:
    """
    Build a MultipartWriter for sending a response to a Telegram webhook.

    Args:
        bot (Bot): The instance of the Bot to use for handled requests.
        result (Optional[TelegramMethod[TelegramType]]): The result of a Telegram method call.

    Returns:
        Optional[MultipartWriter]: A writer for the multipart/form-data request, or None if no result.
    """
    
    # Create MultipartWriter with optional boundary
    mpwriter = MultipartWriter('form-data', f"webhookBoundary{secrets.token_urlsafe(16)}")
    
    # If no result is provided or result is not a TelegramMethod, return None
    if not result or not isinstance(result, TelegramMethod):
        return mpwriter

    # Prepare a dictionary to store file attachments
    files: Dict[str, InputFile] = {}
    
    # Add method as the first part
    method_part = mpwriter.append(result.__api_method__)
    method_part.set_content_disposition('form-data', name='method')

    # Iterate through all result attributes and prepare their values
    for key, value in result.model_dump(warnings=False).items():
        # Prepare the value, converting it to a format suitable for sending
        prepared_value = bot.session.prepare_value(value, bot=bot, files=files)
        
        if prepared_value is not None:
            # Add each non-file value as a part
            part = mpwriter.append(prepared_value)
            part.set_content_disposition('form-data', name=key)

    # Append any file attachments to the writer
    for key, file in files.items():
        file_part = mpwriter.append(file.read(bot))
        file_part.set_content_disposition('form-data', name=key, filename=file.filename)

    return mpwriter