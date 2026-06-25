import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from config import BANNER_FILE, YOUR_TELEGRAM_ID
from data.projects import WELCOME_TEXT, ABOUT_TEXT, HELP_TEXT
from keyboards.inline import (
    get_main_keyboard,
    get_contact_keyboard,
)
from utils import simulate_typing, is_user_rate_limited, safe_edit
from handlers.rating import track_user, load_stats

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state):
    user = message.from_user
    logger.info("User %s (@%s | ID: %s) started the bot", user.full_name, user.username, user.id)

    track_user(user.id, user.full_name, user.username)

    await state.clear()

    if await is_user_rate_limited(user.id):
        return

    from aiogram.types import FSInputFile

    try:
        banner = FSInputFile(BANNER_FILE)
        await message.answer_photo(photo=banner, caption=WELCOME_TEXT, reply_markup=get_main_keyboard())
    except Exception as e:
        logger.warning("Failed to load banner: %s", e)
        await message.answer(WELCOME_TEXT, reply_markup=get_main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT, reply_markup=get_main_keyboard())


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if message.from_user.id != YOUR_TELEGRAM_ID:
        await message.answer("⛔ У вас нет доступа к этой команде.")
        return

    stats = load_stats()
    users = stats.get("users", {})
    total_users = len(users)
    total_views = stats.get("views", 0)
    ratings = stats.get("ratings", [])
    total_ratings = len(ratings)
    avg_rating = sum(r["rating"] for r in ratings) / total_ratings if total_ratings else 0

    rating_map = {}
    for r in ratings:
        rating_map[str(r["user_id"])] = r["rating"]

    lines = [
        "📊 <b>Полная статистика бота</b>\n",
        f"👥 Пользователей: <b>{total_users}</b>",
        f"👀 Всего запусков /start: <b>{total_views}</b>",
        f"⭐ Оценок: <b>{total_ratings}</b> (средняя: <b>{avg_rating:.1f}</b>)",
        "\n<b>Кто запускал бота:</b>",
    ]

    for uid, info in users.items():
        name = info.get("name", "Неизвестно")
        uname = info.get("username")
        starts = info.get("starts", 0)
        tag = f"@{uname}" if uname else "нет юзернейма"
        user_rating = rating_map.get(uid)
        if user_rating:
            rating_str = f" — ⭐ {user_rating}/5"
        else:
            rating_str = " — не голосовал"
        lines.append(f"  • <b>{name}</b> ({tag}) — {starts} запусков{rating_str}")

    await message.answer("\n".join(lines))


@router.callback_query(F.data == "show_about")
async def show_about(callback: CallbackQuery):
    await callback.answer()
    await safe_edit(callback.message, caption=ABOUT_TEXT, reply_markup=get_contact_keyboard())


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state):
    await callback.answer()
    await state.clear()
    await safe_edit(callback.message, text=WELCOME_TEXT, caption=WELCOME_TEXT, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "noop")
async def noop_cb(callback: CallbackQuery):
    await callback.answer()
