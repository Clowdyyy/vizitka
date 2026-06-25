import asyncio
import time
import logging
from collections import defaultdict
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)

_bot: Bot = None
_rate_limit_cache: dict[int, float] = {}
RATE_LIMIT_SECONDS = 1.0


def init_bot(bot: Bot):
    global _bot
    _bot = bot


async def delete_old_message(message):
    try:
        await message.delete()
    except TelegramBadRequest:
        pass


async def simulate_typing(chat_id: int, delay: float = 0.8):
    try:
        await _bot.send_chat_action(chat_id, "typing")
        await asyncio.sleep(delay)
    except Exception:
        pass


async def is_user_rate_limited(user_id: int) -> bool:
    now = time.time()
    last = _rate_limit_cache.get(user_id, 0)
    if now - last < RATE_LIMIT_SECONDS:
        return True
    _rate_limit_cache[user_id] = now
    return False


async def safe_edit(message, text: str = None, caption: str = None, reply_markup=None):
    """Попытка отредактировать сообщение. Если не получается — удаляет старое и шлёт новое."""
    from aiogram.types import InlineKeyboardMarkup

    is_photo = message.photo

    try:
        if caption is not None and is_photo:
            await message.edit_caption(caption=caption, reply_markup=reply_markup)
        elif text is not None:
            await message.edit_text(text=text, reply_markup=reply_markup)
        else:
            return
        return
    except TelegramBadRequest:
        pass

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    if caption is not None and is_photo:
        await _bot.send_photo(chat_id=message.chat.id, photo=message.photo[-1].file_id, caption=caption, reply_markup=reply_markup)
    elif text is not None:
        await _bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup)
