import asyncio
import logging
import signal
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from utils import init_bot

from handlers.common import router as common_router
from handlers.carousel import router as carousel_router
from handlers.stack import router as stack_router
from handlers.rating import router as rating_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher):
    dp.include_router(common_router)
    dp.include_router(carousel_router)
    dp.include_router(stack_router)
    dp.include_router(rating_router)


async def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TOKEN_HERE":
        logger.error("BOT_TOKEN not set! Create .env file with your token.")
        sys.exit(1)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    init_bot(bot)

    dp = Dispatcher()
    setup_handlers(dp)

    logger.info("Bot started successfully!")

    stop_event = asyncio.Event()

    def signal_handler():
        logger.info("Shutdown signal received...")
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, signal_handler)
        except NotImplementedError:
            pass

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
