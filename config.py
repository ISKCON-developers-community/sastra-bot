import os
from dotenv import load_dotenv


load_dotenv()
users_db_file = 'files/users.txt'
logfile = 'files/main.log'
ROOT_ID = int(os.getenv('ROOT_ID'))
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
set_memory = 'self' # 'redis' or 'self'
