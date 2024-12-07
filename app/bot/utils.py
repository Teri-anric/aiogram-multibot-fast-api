"""
Utility functions for Telegram bot webhook response handling.

This module provides utility functions to build multipart responses
for Telegram bot webhook updates, with support for various data types
and file attachments.
"""

import secrets
import json
from typing import Dict, Optional, Generator, Any, Union

from aiogram import Bot
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType
from aiogram.types import InputFile
from fastapi import Response
from fastapi.responses import StreamingResponse

def generate_multipart_telegram_response(
    bot: Bot, 
    result: TelegramMethod[TelegramType], 
    boundary: str
) -> Generator[bytes, None, None]:
    """
    Generate a multipart/form-data response for Telegram webhook.

    Args:
        bot (Bot): The instance of the Bot to use for handled requests.
        result (TelegramMethod[TelegramType]): The result of a Telegram method call.
        boundary (str): Custom boundary for multipart data.

    Yields:
        bytes: Multipart form-data chunks
    """
    # Prepare a dictionary to store file attachments
    files: Dict[str, InputFile] = {}
    
    # Prepare method and its parameters
    method_data = result.model_dump(warnings=False)
    
    # Yield method part
    method_part = (
        f'--{boundary}\r\n'
        'Content-Disposition: form-data; name="method"\r\n'
        'Content-Type: text/plain; charset=utf-8\r\n\r\n'
        f'{result.__api_method__}\r\n'
    )
    yield method_part.encode('utf-8')

    # Process non-file parameters
    for key, value in method_data.items():
        # Prepare the value, converting it to a format suitable for sending
        prepared_value = bot.session.prepare_value(value, bot=bot, files=files)
        
        if prepared_value is not None:
            # Convert value to string for text parts
            if isinstance(prepared_value, (dict, list)):
                prepared_value = json.dumps(prepared_value)
            
            part = (
                f'--{boundary}\r\n'
                f'Content-Disposition: form-data; name="{key}"\r\n'
                'Content-Type: text/plain; charset=utf-8\r\n\r\n'
                f'{prepared_value}\r\n'
            )
            yield part.encode('utf-8')

    # Process file attachments
    for key, file in files.items():
        # Read file content
        file_content = file.read(bot)
        
        # Yield file part headers
        file_part_header = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="{key}"; filename="{file.filename}"\r\n'
            f'Content-Type: application/octet-stream\r\n\r\n'
        )
        yield file_part_header.encode('utf-8')
        
        # Yield file content
        yield file_content
        yield b'\r\n'

    # Final boundary
    yield f'--{boundary}--\r\n'.encode('utf-8')


def build_multipart_response(
    bot: Bot, 
    result: Any
) -> Response:
    if not result or not isinstance(result, TelegramMethod):
        return Response(status_code=200)

    boundary = f"webhookBoundary{secrets.token_urlsafe(16)}"
    return StreamingResponse(
        generate_multipart_telegram_response(bot, result, boundary), 
        media_type=f"multipart/form-data; boundary={boundary}",
        status_code=200
    )
