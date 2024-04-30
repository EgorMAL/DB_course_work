import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from os import getenv
import asyncio

import dotenv

from bot.handlers.admin_panel import router as admin_panel_router

dotenv.load_dotenv()


async def main() -> None:
    bot = Bot(token=getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(admin_panel_router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())