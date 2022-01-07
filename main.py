from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
import os
from dotenv import load_dotenv
import logging
from parse_vedabase import get_full_verse

# q = 'ru sb 1.3.10'

logfile = 'data.log'

logging.basicConfig(filename=logfile,
                    format='%(asctime)s %(levelname)-2s %(message)s',
                    filemode='a',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
load_dotenv()
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Обрабатывает команды `/start` и `/help`
    """
    user_info = [
        str(message.from_user.id),
        message.from_user.first_name,
        dict(message.from_user).get(
            'last_name', 'None'),
        dict(message.from_user).get('username', 'None')
    ]
    logging.info(' | '.join(user_info))
    await message.reply("""To find the verse from the scripture, enter:
- start with 'verse '
- then enter the desired language ('en', 'nl', 'ru', 'da', 'et', 'sk', 'es', 'de', 'uk', 'lt', 'sl', 'fi', 'cs', 'hu', 'fr', 'ko', 'pt-br', 'bg', 'ja', 'zu')

BG: 'verse ru bg 10.8'
SB: 'verse uk sb 1.10.8'
CC (adi, madhya, antya): 'verse en cc adi 10.8'""")


@dp.message_handler(lambda message: message.text.startswith("verse "))
async def search_verse(message: types.Message):
    if len(message.text.split()) < 4 or len(message.text.split()) > 5:
        return await message.reply('Wrong query string. Try /help command')

    query_string = message.text.split('verse ')[1]
    verse = get_full_verse(query_string)
    if 'errors' in verse:
        logging.warning(
            f"{message.text.split('verse ')[1]} - {' | '.join(verse['errors'])}")
        await message.reply('\n'.join(verse['errors']))
    else:
        # logging.info(message.text.split('verse ')[1])
        await message.reply('\n\n'.join(list(verse.values())[:-1]))


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Do not understand this message. Try /help command",  reply_markup=None)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
