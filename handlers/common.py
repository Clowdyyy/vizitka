import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BANNER_FILE, YOUR_TELEGRAM_ID
from data.projects import WELCOME_TEXT, ABOUT_TEXT, HELP_TEXT, CONTACT_PROMPT, CONTACT_SENT
from keyboards.inline import (
    get_main_keyboard,
    get_contact_keyboard,
    get_stats_keyboard,
    get_contact_form_keyboard,
)
from utils import simulate_typing, is_user_rate_limited, safe_edit
from handlers.rating import track_user, load_stats

router = Router()
logger = logging.getLogger(__name__)


class ContactForm(StatesGroup):
    waiting_message = State()


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

    await _show_stats_page(message, page=1)


@router.callback_query(F.data.startswith("stats_page:"))
async def stats_page_callback(callback: CallbackQuery):
    if callback.from_user.id != YOUR_TELEGRAM_ID:
        await callback.answer("⛔ Нет доступа.", show_alert=True)
        return

    await callback.answer()
    try:
        page = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        return

    await _show_stats_page(callback.message, page)


async def _show_stats_page(message, page: int):
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

    per_page = 10
    total_pages = max(1, (total_users + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))

    user_items = list(users.items())
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_users = user_items[start_idx:end_idx]

    header = (
        "📊 <b>Панель управления</b>\n\n"
        f"👥 Пользователей: <b>{total_users}</b> | "
        f"👀 Запусков: <b>{total_views}</b> | "
        f"⭐ Средняя: <b>{avg_rating:.1f}</b>\n\n"
        f"<b>Пользователи (стр. {page}/{total_pages}):</b>\n"
    )

    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    lines = [header]
    for i, (uid, info) in enumerate(page_users):
        name = info.get("name", "Неизвестно")
        uname = info.get("username")
        starts = info.get("starts", 0)
        last_seen = info.get("last_seen", "—")
        tag = f"@{uname}" if uname else "нет юзернейма"
        user_rating = rating_map.get(uid)
        rating_str = f"⭐ {user_rating}/5" if user_rating else "не голосовал"

        emoji = emojis[i] if i < len(emojis) else "▫️"
        lines.append(
            f"{emoji} <b>{name}</b> ({tag})\n"
            f"   🚀 {starts} запусков | 📅 {last_seen}\n"
            f"   {rating_str}"
        )

    text = "\n\n".join(lines)
    keyboard = get_stats_keyboard(page, total_pages)

    from utils import safe_edit
    await safe_edit(message, text=text, reply_markup=keyboard)


@router.callback_query(F.data == "show_about")
async def show_about(callback: CallbackQuery):
    await callback.answer()
    await safe_edit(callback.message, caption=ABOUT_TEXT, reply_markup=get_contact_keyboard())


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state):
    await callback.answer()
    await state.clear()
    await safe_edit(callback.message, text=WELCOME_TEXT, caption=WELCOME_TEXT, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "write_to_author")
async def write_to_author(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ContactForm.waiting_message)
    await safe_edit(callback.message, text=CONTACT_PROMPT, reply_markup=get_contact_form_keyboard())


@router.message(ContactForm.waiting_message)
async def handle_contact_message(message: Message, state: FSMContext):
    await state.clear()

    user = message.from_user
    name = user.full_name
    uname = f"@{user.username}" if user.username else "нет юзернейма"

    admin_text = (
        f"📩 <b>Новое сообщение от пользователя!</b>\n\n"
        f"👤 <b>{name}</b> ({uname})\n"
        f"🆔 ID: <code>{user.id}</code>\n\n"
        f"💬 {message.text}"
    )

    try:
        await message.bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=admin_text)
    except Exception as e:
        logger.error("Failed to send contact message to admin: %s", e)

    await message.answer(CONTACT_SENT, reply_markup=get_main_keyboard())


@router.callback_query(F.data == "noop")
async def noop_cb(callback: CallbackQuery):
    await callback.answer()
