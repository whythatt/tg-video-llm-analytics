import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.llm import query_generation

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("📊 <b>Видеоаналитика бот</b>")


@dp.message(F.text)
async def analytics_handler(message: Message):
    try:
        await message.answer("🔄 Анализирую запрос...")

        # Отправляем в LLM
        llm_result = await query_generation(message.text)

        await message.answer(f"{llm_result}")

    except Exception as e:
        logging.error(f"Ошибка обработки: {e}")
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
