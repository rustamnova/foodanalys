import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Init API keys
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Init OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Init Telegram bot
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

logging.basicConfig(level=logging.INFO)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("👋 Привет! Пришли мне фото состава продукта, и я проанализирую его.")

@router.message(F.photo)
async def handle_photo(message: Message):
    # Получаем наибольшее по размеру фото
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path

    # Скачиваем фото
    photo_bytes = await bot.download_file(file_path)

    # Отправляем в GPT Vision
    gpt_response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "Ты нутрициолог. Проанализируй состав продукта, найди вредные вещества, добавки и аллергены. Кратко и понятно."},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{photo_bytes.read().encode('base64').decode()}", "detail": "low"}}
                ]
            }
        ],
        max_tokens=1000
    )

    result = gpt_response.choices[0].message.content
    await message.answer(f"📋 Вот анализ состава:\n\n{result}", parse_mode=ParseMode.MARKDOWN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
