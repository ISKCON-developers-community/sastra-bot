import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from config import BOT_TOKEN, logfile, ROOT_ID
from help import get_help
from parse_vedabase import get_full_verse
from statiscics import Statisctic
from memory import memory

statistic = Statisctic()

mainlogger = logging.getLogger(__name__)
mainlogger.setLevel(logging.INFO)
handler = logging.FileHandler(logfile)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)-2s %(message)s'))
mainlogger.addHandler(handler)

aiogramlogger = logging.getLogger("aiogram")
aiogramlogger.addHandler(handler)
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
    # TODO russian and english help
    lang = message.from_user.locale.language
    await message.reply(get_help(lang))


@dp.message_handler(lambda message: message.text.lower().startswith("verse "))
async def search_verse(message: types.Message):
    message_text = message.text.lower()
    if len(message_text.split()) < 4 or len(message_text.split()) > 5:
        return await message.reply('Wrong query string. Try /help command')
    query_string = message_text.split('verse ')[1]
    verse = get_full_verse(query_string)
    if 'errors' in verse:
        # TODO errors to statistic
        logging.warning(
            f"{message_text.split('verse ')[1]} - {' | '.join(verse['errors'])}")
        await message.reply('\n'.join(verse['errors']))
    else:
        statistic.write_entry(
                f'{message.from_user.id}:{message.from_user.username}:\
{message.from_user.first_name}:{message.from_user.last_name}',
                verse['purport_id'])
        if not verse['is_purport']:
            watch_purport = '\nNo purport!'
        else:
            watch_purport = f"\n===============\nClick to read purport /purport_{verse['purport_id']}"
        await message.reply('\n\n'.join(list(verse.values())[:-2]) + watch_purport)

@dp.message_handler(commands=['stat'])
async def get_statistics(message: types.Message):
    if message.from_user.id == ROOT_ID:
            await bot.send_document(
                message.from_user.id,
                open('files/stat.log', 
                'rb'))


@dp.message_handler(lambda message: message.text.startswith("/message "))
async def sendind_to_users(message: types.Message):
    if message.from_user.id == ROOT_ID:
        for user in []:
            await bot.send_message(user, message.text.replace('/message ', ''))


@dp.message_handler(lambda message: message.text.startswith("/purport_"))
async def sendind_purport(message: types.Message):
    purport_id = message.text.replace('/purport_', '')
    try:
        await message.reply(memory.get(purport_id))
    except KeyError:
        await message.reply(f'The link is out of date. You need to re-enter the verse number to getting text and comment.\nEx. verse en sb 1.10.8')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Do not understand this message. Try /help command",  reply_markup=None)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
