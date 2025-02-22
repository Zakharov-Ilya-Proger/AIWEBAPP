from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):

    class Config:
        env_file = '.env'

load_dotenv()
settings = Settings()