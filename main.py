import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from config import users_db_file, BOT_TOKEN, logfile, ROOT_ID
from parse_vedabase import get_full_verse
from users import Users

users_db = Users(users_db_file)
logging.basicConfig(filename=logfile,
                    format='%(asctime)s %(levelname)-2s %(message)s',
                    filemode='a',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Обрабатывает команды `/start` и `/help`
    """
    # user_info = [
    #     str(message.from_user.id),
    #     message.from_user.first_name,
    #     dict(message.from_user).get(
    #         'last_name', 'None'),
    #     dict(message.from_user).get('username', 'None')
    # ]
    users_db.add_user(message.from_user.id)
    await message.reply("""To find the verse from the scripture, enter:
- start with 'verse '
- then enter the desired language ('en', 'nl', 'ru', 'da', 'et', 'sk', 'es', 'de', 'uk', 'lt', 'sl', 'fi', 'cs', 'hu', 'fr', 'ko', 'pt-br', 'bg', 'ja', 'zu')

BG: 'verse ru bg 10.8'
SB: 'verse uk sb 1.10.8'
CC (adi, madhya, antya): 'verse en cc adi 10.8'""")


@dp.message_handler(lambda message: message.text.lower().startswith("verse "))
async def search_verse(message: types.Message):
    message_text = message.text.lower()
    if len(message_text.split()) < 4 or len(message_text.split()) > 5:
        return await message.reply('Wrong query string. Try /help command')

    query_string = message_text.split('verse ')[1]
    verse = get_full_verse(query_string)
    if 'errors' in verse:
        logging.warning(
            f"{message_text.split('verse ')[1]} - {' | '.join(verse['errors'])}")
        await message.reply('\n'.join(verse['errors']))
    else:
        # logging.info(message_text.split('verse ')[1])
        await message.reply('\n\n'.join(list(verse.values())[:-1]))


@dp.message_handler(lambda message: message.text.startswith("/message "))
async def sendind_to_users(message: types.Message):
    if message.from_user.id == ROOT_ID:
        for user in users_db.users:
            await bot.send_message(user, message.text.replace('/message ', ''))


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Do not understand this message. Try /help command",  reply_markup=None)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
