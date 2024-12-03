"""
Configuration settings for the Telegram bot application.

This module defines and loads environment-specific configuration
parameters used throughout the application.
"""

from pydantic_settings import BaseSettings
from pydantic import HttpUrl

class Settings(BaseSettings):
    """
    Application configuration settings.

    Loads settings from environment variables or .env file.
    """
    bot_token: str
    web_url: HttpUrl

SETTINGS = Settings()