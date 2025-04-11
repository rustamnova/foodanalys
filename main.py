import logging
import os
import base64
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from io import BytesIO
from openai import OpenAI

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация OpenAI клиента
client = OpenAI(api_key=OPENAI_API_KEY)

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация Telegram-бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Стартовое сообщение
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("👋 Привет! Пришли мне фото состава продукта, и я проанализирую его при помощи нейросети GPT.")

# Обработка фотографии
@router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer("📷 Загружаю изображение и передаю в нейросеть...")

    try:
        # Получаем наибольшее фото
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        photo_path = file.file_path

        # Скачиваем изображение
        photo_bytes = await bot.download_file(photo_path)
        image_bytes = photo_bytes.read()

        # Кодируем в base64
        b64_image = base64.b64encode(image_bytes).decode("utf-8")

        await message.answer("🧠 GPT анализирует состав...")

        # Отправляем картинку в GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Ты нутрициолог. На изображении — состав продукта. Извлеки его и проанализируй: выдели вредные добавки, аллергены, синтетические вещества. Дай краткий и понятный вывод."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Проанализируй состав на фото."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        result = response.choices[0].message.content
        await message.answer(f"📋 Анализ состава:\n\n{result}", parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logging.error(f"Ошибка GPT: {e}")
        await message.answer("⚠️ Ошибка при анализе изображения. Попробуй позже или пришли другое фото.")

# Запуск бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
