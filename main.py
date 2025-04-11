import logging
import os
import base64
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from io import BytesIO
from openai import OpenAI

# Загрузка .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация
client = OpenAI(api_key=OPENAI_API_KEY)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)
logging.basicConfig(level=logging.INFO)

# Кнопки
def analysis_options_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💊 Добавки (E-компоненты)", callback_data="filter_additives")],
        [InlineKeyboardButton(text="🧠 Влияние на здоровье", callback_data="filter_health")],
        [InlineKeyboardButton(text="🌾 Аллергены", callback_data="filter_allergens")],
    ])

# Основной промпт для изображения
image_analysis_prompt = (
    "Ты нутрициолог. На изображении — упаковка с составом продукта. "
    "Извлеки текст и проанализируй его: укажи вредные вещества, добавки, аллергены. "
    "Ответь кратко и структурировано."
)

# Старт
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("👋 Привет! Пришли мне фото состава продукта, и я проанализирую его.")

# Фото
@router.message(F.photo)
async def handle_photo(message: Message, state: FSMContext):
    await message.answer("📷 Загружаю изображение...")

    try:
        # Получаем изображение
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        photo_data = await bot.download_file(file_info.file_path)
        image_bytes = photo_data.read()
        b64_image = base64.b64encode(image_bytes).decode("utf-8")

        logging.info("▶️ Загружено изображение от пользователя %s", message.from_user.id)
        logging.info("🧠 Промпт для анализа изображения:\n%s", image_analysis_prompt)

        await message.answer("🧠 GPT анализирует состав...")

        # Первый анализ
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": image_analysis_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Вот изображение упаковки:"},
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
        logging.info("✅ Ответ от GPT (анализ изображения):\n%s", result)

        await state.update_data(last_text=result)

        await message.answer(f"📋 Вот анализ состава:\n\n{result}", parse_mode=ParseMode.MARKDOWN)
        await message.answer("🔎 Что хочешь узнать подробнее?", reply_markup=analysis_options_kb())

    except Exception as e:
        logging.error("❌ Ошибка анализа изображения: %s", e)
        await message.answer("⚠️ Ошибка при анализе. Попробуй позже.")

# Обработка кнопок
@router.callback_query(F.data.startswith("filter_"))
async def handle_filter(callback: CallbackQuery, state: FSMContext):
    await callback.answer("🔄 Переанализирую...")

    data = await state.get_data()
    text = data.get("last_text")

    if not text:
        await callback.message.answer("⚠️ Нет текста для анализа. Пришли фото сначала.")
        return

    filters = {
        "filter_additives": "Проанализируй текст на наличие пищевых добавок (E-компонентов), например E120, E621 и т.п. Опиши их свойства и возможный вред.",
        "filter_health": "Оцени, как состав влияет на здоровье человека: ЖКТ, печень, сердце, эндокринную, нервную системы.",
        "filter_allergens": "Найди возможные аллергены в тексте. Подчеркни те, что особенно опасны для чувствительных людей (глютен, молоко, яйца, орехи, соя и т.п.).",
    }

    system_prompt = filters.get(callback.data)
    logging.info("📌 Выбран фильтр: %s", callback.data)
    logging.info("🧠 Промпт для уточнённого анализа:\n%s", system_prompt)
    logging.info("📄 Используемый текст:\n%s", text)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            max_tokens=1000
        )

        answer = response.choices[0].message.content
        logging.info("✅ Ответ от GPT (по фильтру):\n%s", answer)

        await callback.message.answer(f"🔍 Результат:\n\n{answer}", parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logging.error("❌ Ошибка повторного анализа: %s", e)
        await callback.message.answer("⚠️ Ошибка при повторном анализе. Попробуй позже.")

# Запуск
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
