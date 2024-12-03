from pydantic_settings import BaseSettings
from pydantic import HttpUrl

class Settings(BaseSettings):
    bot_token: str
    web_url: HttpUrl

SETTINGS = Settings()