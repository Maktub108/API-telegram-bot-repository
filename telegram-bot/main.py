import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile
from deep_translator import GoogleTranslator
from docx import Document

from tts import gTTS

from config import TOKEN

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

IMG_FOLDER = "img"
bot = Bot(token=TOKEN)
dp = Dispatcher()



@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile("video.mp4")
    await bot.send_video(message.chat.id,video)

@dp.message(lambda message: message.photo)
async def save_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, f"img/{file_id}.jpg")


@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("TG02.pdf")
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio= FSInputFile("audio.mp3")
    await bot.send_video(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "🏋️‍♂️ Тренировка 1: Круговой комплекс\n, 1. Приседания - 3х15\n, 2. Отжимания - 3х12\n, 3. Планка - 3х30 сек\n\n, 4. Подтягивания - 3х8 (или австралийские подтягивания)\n, 5. Скручивания на пресс - 3х20",
        "🔥 Тренировка 2: Интервальная (HIIT)\n, 1. Берпи - 30 сек / отдых 15 сек\n, 2. Прыжки через скакалку - 45 сек / отдых 15 сек\n, 3. Альпинист - 30 сек / отдых 15 сек\n, 4. Приседания с прыжком - 30 сек / отдых 15 сек\n"
        "💪 Тренировка 3: На выносливость\n, 1. Бег или быстрая ходьба - 20 мин\n, 2. Отжимания - 4х15\n, 3. Приседания - 4х20\n, 4. Планка - 1 мин (3 подхода)\n, 5. Подъем ног на пресс - 3х15"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини тренировка на сегодня {rand_tr}")

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.ogg")
    audio = FSInputFile('training.ogg')
    await bot.send_audio(message.chat.id, audio)
    os.remove("training.ogg")


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
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/minitraining")

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
