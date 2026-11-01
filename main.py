import asyncio
import logging
import os
from contextlib import suppress
from dotenv import load_dotenv

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from scraper import fetch_github_bounties

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN не найден в .env")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Создаем клавиатуру с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="▶️ Поиск Bounty")],
        [KeyboardButton(text="⏹ Стоп")],
    ],
    resize_keyboard=True,
)

is_running = False
monitor_task: asyncio.Task[None] | None = None
monitor_chat_id: int | None = None
seen_ids: set[int] = set()
MONITOR_INTERVAL_SECONDS = 300
logger = logging.getLogger(__name__)


async def monitor_loop() -> None:
    while is_running:
        try:
            bounties = await fetch_github_bounties()
            for bounty in bounties:
                bounty_id = bounty["id"]
                if not isinstance(bounty_id, int) or bounty_id in seen_ids:
                    continue
                if monitor_chat_id is None:
                    raise RuntimeError("Monitor chat ID is not configured.")

                await bot.send_message(
                    chat_id=monitor_chat_id,
                    text=f"🎯 {bounty['title']}\n{bounty['url']}",
                )
                seen_ids.add(bounty_id)
        except asyncio.CancelledError:
            raise
        except (
            aiohttp.ClientError,
            asyncio.TimeoutError,
            TelegramAPIError,
            ValueError,
        ):
            logger.exception("Bounty monitoring iteration failed.")

        if is_running:
            await asyncio.sleep(MONITOR_INTERVAL_SECONDS)


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я бот-снайпер для поиска Bounty. Нажми кнопку ниже, чтобы начать мониторинг.",
        reply_markup=keyboard,
    )


@dp.message(F.text == "▶️ Поиск Bounty")
async def start_search(message: Message) -> None:
    global is_running, monitor_task, monitor_chat_id
    if is_running:
        await message.answer("Мониторинг уже запущен.")
        return

    monitor_chat_id = message.chat.id
    is_running = True
    monitor_task = asyncio.create_task(monitor_loop())
    await message.answer(
        "🔎 Запускаю поиск Bounty..."
    )


@dp.message(F.text == "⏹ Стоп")
async def stop_search(message: Message) -> None:
    global is_running, monitor_task
    if not is_running:
        await message.answer("Мониторинг и так остановлен.")
        return

    is_running = False
    task = monitor_task
    monitor_task = None
    if task is not None:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
    await message.answer("⏹ Мониторинг остановлен.")


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
