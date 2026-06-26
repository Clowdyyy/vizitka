import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BANNER_FILE, YOUR_TELEGRAM_ID
from data.translations import (
    WELCOME, ABOUT, HELP, CONTACT_PROMPT, CONTACT_SENT,
    LANG_CHOICE, LANG_SELECTED,
)
from keyboards.inline import (
    get_main_keyboard,
    get_contact_keyboard,
    get_stats_keyboard,
    get_contact_form_keyboard,
    get_lang_keyboard,
)
from utils import simulate_typing, is_user_rate_limited, safe_edit
from handlers.rating import track_user, load_stats, save_stats

router = Router()
logger = logging.getLogger(__name__)

_reply_map: dict[int, int] = {}


def get_lang(user_id: int) -> str:
    stats = load_stats()
    return stats.get("users", {}).get(str(user_id), {}).get("lang", "ru")


def set_lang(user_id: int, lang: str):
    stats = load_stats()
    uid = str(user_id)
    if uid not in stats["users"]:
        stats["users"][uid] = {"name": "", "username": None, "first_seen": "", "last_seen": "", "starts": 0}
    stats["users"][uid]["lang"] = lang
    save_stats(stats)


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

    lang = get_lang(user.id)
    from aiogram.types import FSInputFile

    try:
        banner = FSInputFile(BANNER_FILE)
        await message.answer_photo(photo=banner, caption=WELCOME[lang], reply_markup=get_main_keyboard(lang))
    except Exception as e:
        logger.warning("Failed to load banner: %s", e)
        await message.answer(WELCOME[lang], reply_markup=get_main_keyboard(lang))


@router.message(Command("help"))
async def cmd_help(message: Message):
    lang = get_lang(message.from_user.id)
    await message.answer(HELP[lang], reply_markup=get_main_keyboard(lang))


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if message.from_user.id != YOUR_TELEGRAM_ID:
        await message.answer("\u26d4 \u0423 \u0432\u0430\u0441 \u043d\u0435\u0442 \u0434\u043e\u0441\u0442\u0443\u043f\u0430 \u043a \u044d\u0442\u043e\u0439 \u043a\u043e\u043c\u0430\u043d\u0434\u0435.")
        return

    await _show_stats_page(message, page=1)


@router.callback_query(F.data.startswith("stats_page:"))
async def stats_page_callback(callback: CallbackQuery):
    if callback.from_user.id != YOUR_TELEGRAM_ID:
        await callback.answer("\u26d4 \u041d\u0435\u0442 \u0434\u043e\u0441\u0442\u0443\u043f\u0430.", show_alert=True)
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
        "\U0001f4ca <b>\u041f\u0430\u043d\u0435\u043b\u044c \u0443\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u044f</b>\n\n"
        f"\U0001f465 \u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439: <b>{total_users}</b> | "
        f"\U0001f440 \u0417\u0430\u043f\u0443\u0441\u043a\u043e\u0432: <b>{total_views}</b> | "
        f"\u2b50 \u0421\u0440\u0435\u0434\u043d\u044f\u044f: <b>{avg_rating:.1f}</b>\n\n"
        f"<b>\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438 (\u0441\u0442\u0440. {page}/{total_pages}):</b>\n"
    )

    emojis = ["1\ufe0f\u20e3", "2\ufe0f\u20e3", "3\ufe0f\u20e3", "4\ufe0f\u20e3", "5\ufe0f\u20e3", "6\ufe0f\u20e3", "7\ufe0f\u20e3", "8\ufe0f\u20e3", "9\ufe0f\u20e3", "\U0001f51f"]

    lines = [header]
    for i, (uid, info) in enumerate(page_users):
        name = info.get("name", "\u041d\u0435\u0438\u0437\u0432\u0435\u0441\u0442\u043d\u043e")
        uname = info.get("username")
        starts = info.get("starts", 0)
        last_seen = info.get("last_seen", "\u2014")
        tag = f"@{uname}" if uname else "\u043d\u0435\u0442 \u044e\u0437\u0435\u0440\u043d\u0435\u0439\u043c\u0430"
        user_rating = rating_map.get(uid)
        rating_str = f"\u2b50 {user_rating}/5" if user_rating else "\u043d\u0435 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043b"

        emoji = emojis[i] if i < len(emojis) else "\u2ab\ufe0f"
        lines.append(
            f"{emoji} <b>{name}</b> ({tag})\n"
            f"   \U0001f680 {starts} \u0437\u0430\u043f\u0443\u0441\u043a\u043e\u0432 | \U0001f4c5 {last_seen}\n"
            f"   {rating_str}"
        )

    text = "\n\n".join(lines)
    keyboard = get_stats_keyboard(page, total_pages)

    from utils import safe_edit
    await safe_edit(message, text=text, reply_markup=keyboard)


@router.callback_query(F.data == "show_about")
async def show_about(callback: CallbackQuery):
    await callback.answer()
    lang = get_lang(callback.from_user.id)
    await safe_edit(callback.message, caption=ABOUT[lang], reply_markup=get_contact_keyboard())


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state):
    await callback.answer()
    await state.clear()
    lang = get_lang(callback.from_user.id)
    await safe_edit(callback.message, text=WELCOME[lang], caption=WELCOME[lang], reply_markup=get_main_keyboard(lang))


@router.callback_query(F.data == "change_lang")
async def change_lang(callback: CallbackQuery):
    await callback.answer()
    lang = get_lang(callback.from_user.id)
    await safe_edit(callback.message, text=LANG_CHOICE[lang], reply_markup=get_lang_keyboard())


@router.callback_query(F.data.startswith("set_lang:"))
async def set_lang_handler(callback: CallbackQuery, state):
    await callback.answer()
    lang = callback.data.split(":")[1]
    set_lang(callback.from_user.id, lang)
    await state.clear()
    await safe_edit(callback.message, text=LANG_SELECTED[lang], reply_markup=get_main_keyboard(lang))


@router.callback_query(F.data == "write_to_author")
async def write_to_author(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ContactForm.waiting_message)
    lang = get_lang(callback.from_user.id)
    await safe_edit(callback.message, text=CONTACT_PROMPT[lang], reply_markup=get_contact_form_keyboard())


@router.message(ContactForm.waiting_message)
async def handle_contact_message(message: Message, state: FSMContext):
    await state.clear()

    user = message.from_user
    name = user.full_name
    uname = f"@{user.username}" if user.username else "\u043d\u0435\u0442 \u044e\u0437\u0435\u0440\u043d\u0435\u0439\u043c\u0430"

    admin_text = (
        f"\U0001f4e9 <b>\u041d\u043e\u0432\u043e\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 \u043e\u0442 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f!</b>\n\n"
        f"\U0001f464 <b>{name}</b> ({uname})\n"
        f"\U0001f194 ID: <code>{user.id}</code>\n\n"
        f"\U0001f4ac {message.text}\n\n"
        f"<i>\u041e\u0442\u0432\u0435\u0442\u044c\u0442\u0435 \u043d\u0430 \u044d\u0442\u043e \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435, \u0447\u0442\u043e\u0431\u044b \u043f\u0435\u0440\u0435\u0441\u043b\u0430\u0442\u044c \u043e\u0442\u0432\u0435\u0442 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044e.</i>"
    )

    try:
        sent = await message.bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=admin_text)
        _reply_map[sent.message_id] = user.id
    except Exception as e:
        logger.error("Failed to send contact message to admin: %s", e)

    lang = get_lang(user.id)
    await message.answer(CONTACT_SENT[lang], reply_markup=get_main_keyboard(lang))


@router.message(F.chat.id == YOUR_TELEGRAM_ID, F.reply_to_message)
async def handle_admin_reply(message: Message):
    reply_to = message.reply_to_message
    user_id = _reply_map.get(reply_to.message_id)
    if not user_id:
        return

    try:
        await message.bot.send_message(
            chat_id=user_id,
            text=f"\U0001f4e9 <b>\u041e\u0442\u0432\u0435\u0442 \u043e\u0442 \u0430\u0432\u0442\u043e\u0440\u0430:</b>\n\n{message.text}",
        )
        lang = get_lang(user_id)
        await message.answer("\u2705 \u041e\u0442\u0432\u0435\u0442 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d.", reply_markup=get_main_keyboard(lang))
    except Exception as e:
        logger.error("Failed to forward reply to user %s: %s", user_id, e)
        await message.answer("\u274c \u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c.", reply_markup=get_main_keyboard())


@router.callback_query(F.data == "noop")
async def noop_cb(callback: CallbackQuery):
    await callback.answer()
