from dotenv import load_dotenv
import os
from pathlib import Path
from sys import exit

load_dotenv()


DATABASE_FILE = "db.sqlite3"
BOT_TOKEN = os.getenv("BOT_TOKEN") or ''
BOT_MODE = os.getenv("BOT_MODE") or "dev"
ROOT_ID = int(os.getenv("ROOT_ID") or 0)
BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_DB_FILE = BASE_DIR / DATABASE_FILE
REDIS_HOST = "localhost"
REDIS_PORT = 6379

errors = []
if not BOT_TOKEN:
    errors.append(" - Не найдена переменная BOT_TOKEN")

if not ROOT_ID:
    errors.append(" - Не найдена переменная ADMIN_ID")

if len(errors):
    print("Внимание! Ошибка запуска. Не найдены переменные окружения. Вам \
необходимо создать файл .env по образцу .env.sample и заполнить в нем значения, \
либо добавить в переменные окружения необходимые данные")
    exit("\n".join(errors))

