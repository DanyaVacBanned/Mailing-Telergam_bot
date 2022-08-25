from aiogram import Bot, Dispatcher, executor, types
import logging, random
from database import Database
from bot_ans_base import HELLO_ANSWERS, MOOD_ANSWERS, HELLO_QUESTIONS, MOOD_QUESTIONS

#DATABASE
db = Database('db.db')

#BOT INITALIZING
logging.basicConfig(level=logging.INFO)
TOKEN = 'Bot Token'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


#BODY

@dp.message_handler(commands='start')
async def get_started(message: types.Message):
    await bot.send_message(message.chat.id, 'HELLO TEXT')
    if not (db.user_exists(message.chat.id)):
        db.add_user(message.chat.id)
        print('Пользователь зарегестрирован!')
    else:
        await bot.send_message(message.chat.id, 'You are allready registred')


@dp.message_handler(commands='sendall')
async def sendall(message: types.Message):
    if message.chat.type =='private':
        if message.from_user.id == 1009429556:
            text = message.text[9:]
            users = db.get_user()
            for row in users:
                #Maybe in future i will be add get active system
                await bot.send_message(row[0], text)

@dp.message_handler()
async def justtext(message: types.Message):
    if message.text.lower() in HELLO_QUESTIONS:
        await bot.send_message(message.chat.id, HELLO_ANSWERS[random.randint(0, len(HELLO_ANSWERS)-1)])

    elif message.text.lower() in MOOD_QUESTIONS:
        await bot.send_message(message.chat.id, MOOD_ANSWERS[random.randint(0, len(MOOD_ANSWERS)-1)])
    else:
        pass

#POLLING
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
