import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from handler import menuDevelopmentHandler
from handler.countries import countryHandler
from handler.start import startingHandler
from config.configurations import TOKEN
from handler.worlds import userUpdateKeyboard


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(TOKEN)
    dp.include_router(startingHandler.router)
    dp.include_router(userUpdateKeyboard.router)
    dp.include_router(countryHandler.router)
    dp.include_router(menuDevelopmentHandler.router)
    # dp.include_router(common.router)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    asyncio.run(main())
