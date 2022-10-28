from aiogram import Bot, Dispatcher, executor, types
import logging, random
from database import Database
from bot_ans_base import HELLO_ANSWERS, MOOD_ANSWERS, HELLO_QUESTIONS, MOOD_QUESTIONS
from aiogram import filters
import configparser
from random import choice
import requests
from bs4 import BeautifulSoup as b
#DATABASE
db = Database('db.db')

#BOT INITALIZING
config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(level=logging.INFO)
TOKEN = config['CONFIG_TELEGRAM']['bot_token']
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
admin_id = int(config['CONFIG_TELEGRAM']['admin_id'])
with open('commands.txt','r',encoding='utf-8') as f:
     commands_list = f.read()
#BODY



@dp.message_handler(commands='start')
async def get_started(message: types.Message):

    if not (db.user_exists(message.chat.id)):
        db.add_user(message.chat.id)
        await bot.send_message(message.chat.id, "Привет! Меня зовут Гоша! Мой создатель поручил мне скидывать вам всякие смешнявые смешнявки! Каждый, кто подписан на меня - будет получать отборные мемесы каждый раз, когда создатель захочет вас порадовать!:)")
        await bot.send_message(message.from_user.id, f'Вы также можете прописать следующие команды, чтобы взаимодейстовать со мной:\n {commands_list}')
        print('Пользователь зарегестрирован!')
    else:
        await bot.send_message(message.chat.id, 'Вы уже зарегестрированы!')



@dp.message_handler(commands='sendall')
async def sendall(message: types.Message):
    if message.from_user.id == admin_id:
        text = message.text[9:]
        print(text)
        users = db.get_user()
        print(users)
        for row in users:
            #Maybe in future i will be add get active system
            await bot.send_message(row[0], text)
            print(row[0])

@dp.message_handler(commands='anekdot')
async def anekdotru(message: types.Message):
    r = requests.get('https://www.anekdot.ru/release/anekdot/year/')
    html = r.text
    soup = b(html, 'lxml')
    anek = soup.find_all('div',class_='text')
    clear_aneks = [c.text for c in anek]
    
    
    await bot.send_message(message.from_user.id, choice(clear_aneks))



@dp.message_handler(filters.Text)
async def justtext(message: types.Message):
    if message.text.lower() in HELLO_QUESTIONS:
        await bot.send_message(message.chat.id, HELLO_ANSWERS[random.randint(0, len(HELLO_ANSWERS)-1)])

    elif message.text.lower() in MOOD_QUESTIONS:
        await bot.send_message(message.chat.id, MOOD_ANSWERS[random.randint(0, len(MOOD_ANSWERS)-1)])

    
    if message.from_user.id != admin_id:
        await bot.send_message(admin_id,f"{message.from_user.first_name}: {message.text}")
    
    





   

#POLLING
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)