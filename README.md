# Shastra-cakshu telegram bot

Telegram bot sends verses from scriptures by requests
Text based requests suports now only

## Deployment with venv or Docker

1. Clone the repo `https://github.com/ISKCON-developers-community/sastra-bot.git`
2. `cd sastra-bot`
3. You can run it in virtual env or in docker. To run in venv python=<3.9
4. Creat virtual env `python 3.9 -m venv env` then acivate it`. env/bin/activate`
5. Instal requirements `pip install -r requirements.txt`
6. Create .env file as copy of .env.sample `cp .env.sample .env`
7. To run bot you need to get bot token from botFather and you must know you own telegram ID
8. Insert this info into .env file
9. Run the bot `python sastrabot.py`
10. For deployment with Docker skip steps 3-5. But you must have Docker installed
11. Run on linux or Mac `make create` and `make run`. To using make command in Windows watch https://earthly.dev/blog/makefiles-on-windows/ or run with related docker commands from Makefile
