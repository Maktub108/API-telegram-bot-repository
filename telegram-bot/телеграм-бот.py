
import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo'))
async def photo(message: Message):
    photos = [
        'https://zoogalaktika.ru/assets/images/aves/psittaciformes/aratinga/aratinga-solstitialis/aratinga-solstitialis_01.jpg',
        'https://i.pinimg.com/736x/1a/84/27/1a842723765df2ddd22ea1e7c8e44df8.jpg',
        'https://i.pinimg.com/736x/cc/ca/e5/cccae50ab566c68d2add0bc7296be793.jpg'
    ]
    rand_photo = random.choice(photos)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(F.photo)
async def react_photo(message: Message):
    answers = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(answers)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer("Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/photo")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Приветики, {message.from_user.full_name}")

@dp.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

