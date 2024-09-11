from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()


class Settings:
    # все обязательные переменные окружения
    # имеет смысл считывать через os.environ[key]
    #
    # чтобы при отсутствии переменной окружения поднималось исключение KeyError
    # и программа не работала
    # через os.getenv(key) - при отсутствии переменной, возвращается None, 
    # что затем усложняет поиск ошибок в программе
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    DB_NAME = os.environ["DB_NAME"]
    DB_SCHEMA = os.environ["DB_SCHEMA"]

    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    HASH_TOKEN = os.environ["HASH_TOKEN"]
    ALGORITHM = os.environ["ALGORITHM"]
print(Settings.ALGORITHM)