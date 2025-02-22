import os

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):

    ALLOWED_USER_IP = os.getenv("ALLOWED_USER_IP")
    GPT_API_KEY = os.getenv("GPT_API_KEY")
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
    REBOOT_HOOK = os.getenv("REBOOT_HOOK")

    class Config:
        env_file = '.env'

load_dotenv()
settings = Settings()