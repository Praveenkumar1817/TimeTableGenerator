from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Timetable Generator API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./timetable.db")

    class Config:
        env_file = ".env"

settings = Settings()
