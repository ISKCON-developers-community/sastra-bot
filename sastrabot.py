import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config.config import BOT_MODE, BOT_TOKEN, LOG_FILE


# ========== LOGGER ==============
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s - %(message)s"
logging.basicConfig(
		filename=LOG_FILE if BOT_MODE == 'prod' else None,
		level=logging.INFO if BOT_MODE == 'prod' else logging.DEBUG,
		format=LOG_FORMAT)
logger = logging.getLogger('SASTRABOT')

logging.getLogger("aiogram").setLevel(logging.DEBUG + 1)
# =======================================

# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Запуск процесса поллинга новых апдейтов
async def main():
    logger.info(f"Bot has been started in {BOT_MODE.upper()} MODE")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
