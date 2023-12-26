import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from backup import create_backup
from callbacks import pagination
from constants.config import TOKEN
from handlers import messages, commands


async def scheduler():
    while True:
        await create_backup()
        await asyncio.sleep(1 * 60 * 60 * 24)


async def main():
    bot = Bot(TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(
        commands.router,
        messages.router,
        pagination.router
    )

    loop = asyncio.get_event_loop()

    # loop.create_task(scheduler())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
