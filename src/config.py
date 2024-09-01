from dotenv import load_dotenv
import os
# Загрузка переменных окружения из файла .env
load_dotenv()

class Settings():
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_NAME = os.getenv('DB_NAME')
    DB_SCHEMA = os.getenv('DB_SCHEMA')
    DATABASE_URL: str = ""

    @classmethod
    def generate_database_url(cls):
        # Генерация DATABASE_URL на основе параметров
        cls.DATABASE_URL = (
            f"postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASS}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        )

settings = Settings()
settings.generate_database_url()