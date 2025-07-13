import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, ACCUWEATHER_API_KEY, CITY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кэш для хранения ключа локации (CITY_KEY)
CITY_KEY = None


async def get_city_key():
    """Получаем уникальный идентификатор города из AccuWeather API"""
    global CITY_KEY
    if CITY_KEY is None:
        try:
            url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={ACCUWEATHER_API_KEY}&q={CITY}"
            response = requests.get(url)
            response.raise_for_status()  # Проверка ошибок HTTP
            data = response.json()
            CITY_KEY = data[0]["Key"]
        except Exception as e:
            raise Exception(f"Ошибка получения ключа города: {str(e)}")
    return CITY_KEY


@dp.message(CommandStart())
async def start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        f"Привет! Я показываю погоду в {CITY}. 🌦️\n"
        "Напиши /weather для получения данных."
    )


@dp.message(Command('weather'))
async def get_weather(message: Message):
    """Получение и вывод данных о погоде"""
    try:
        # 1. Получаем идентификатор города
        city_key = await get_city_key()

        # 2. Запрашиваем текущую погоду
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{city_key}?apikey={ACCUWEATHER_API_KEY}&language=ru"
        response = requests.get(url)
        response.raise_for_status()

        # 3. Извлекаем основные данные
        weather_data = response.json()[0]
        weather_text = weather_data["WeatherText"]
        temperature = weather_data["Temperature"]["Metric"]["Value"]

        # 4. Форматируем ответ
        await message.answer(
            f"🏙 Погода в {CITY}:\n"
            f"• Состояние: {weather_text}\n"
            f"• Температура: {temperature}°C"
        )

    except requests.exceptions.RequestException as e:
        await message.answer("⚠️ Ошибка подключения к сервису погоды.")
    except KeyError:
        await message.answer("⚠️ Неожиданный формат данных от сервера.")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")


async def main():
    """Запуск бота"""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())