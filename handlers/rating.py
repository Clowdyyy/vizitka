import json
import os
import logging
from datetime import datetime, timezone, timedelta
from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.translations import RATING, RATING_ASK, RATING_ALREADY, RATING_DENIED
from keyboards.inline import get_rating_keyboard, get_main_keyboard
from config import YOUR_TELEGRAM_ID
from utils import safe_edit
from handlers.common import get_lang

router = Router()
logger = logging.getLogger(__name__)

STATS_FILE = os.path.join(os.path.dirname(__file__), "..", "stats.json")


def load_stats() -> dict:
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": {}, "views": 0, "ratings": []}


def save_stats(stats: dict):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def track_user(user_id: int, full_name: str, username: str | None):
    stats = load_stats()
    stats["views"] += 1
    uid = str(user_id)
    now = datetime.now(timezone(timedelta(hours=5))).strftime("%d.%m.%Y %H:%M")
    if uid not in stats["users"]:
        stats["users"][uid] = {
            "name": full_name,
            "username": username,
            "first_seen": now,
            "last_seen": now,
            "starts": 0,
        }
    stats["users"][uid]["starts"] += 1
    stats["users"][uid]["last_seen"] = now
    stats["users"][uid]["name"] = full_name
    if username:
        stats["users"][uid]["username"] = username
    save_stats(stats)


@router.callback_query(F.data == "show_rating")
async def show_rating(callback: CallbackQuery):
    await callback.answer()

    stats = load_stats()
    uid = str(callback.from_user.id)
    lang = get_lang(callback.from_user.id)

    for r in stats["ratings"]:
        if str(r.get("user_id")) == uid:
            user_rating = r["rating"]
            text = RATING_ALREADY[lang].format(rating=user_rating)
            await safe_edit(callback.message, text=text, caption=text, reply_markup=get_main_keyboard(lang))
            return

    await safe_edit(callback.message, text=RATING_ASK[lang], caption=RATING_ASK[lang], reply_markup=get_rating_keyboard())


@router.callback_query(F.data == "show_stats")
async def show_stats(callback: CallbackQuery):
    await callback.answer()

    stats = load_stats()
    lang = get_lang(callback.from_user.id)

    if callback.from_user.id == YOUR_TELEGRAM_ID:
        from handlers.common import _show_stats_page
        await _show_stats_page(callback.message, page=1)
    else:
        from data.translations import STATS
        text = STATS[lang].format(
            users=len(stats["users"]),
            views=stats["views"],
            ratings=len(stats["ratings"]),
        )
        await safe_edit(callback.message, text=text, caption=text, reply_markup=get_main_keyboard(lang))


@router.callback_query(F.data.startswith("rate:"))
async def handle_rating(callback: CallbackQuery):
    await callback.answer()

    try:
        rating = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        return

    if rating < 1 or rating > 5:
        return

    stats = load_stats()
    uid = str(callback.from_user.id)
    lang = get_lang(callback.from_user.id)

    for r in stats["ratings"]:
        if str(r.get("user_id")) == uid:
            await safe_edit(callback.message, text=RATING_DENIED[lang], caption=RATING_DENIED[lang], reply_markup=get_main_keyboard(lang))
            return

    stats["ratings"].append({
        "user_id": callback.from_user.id,
        "rating": rating,
        "date": datetime.now().isoformat(),
    })

    if uid in stats["users"]:
        stats["users"][uid]["rating"] = rating

    save_stats(stats)

    stars = "\u2b50" * rating
    text = RATING[lang].format(stars=stars)
    await safe_edit(callback.message, text=text, caption=text, reply_markup=get_main_keyboard(lang))
