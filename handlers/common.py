import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BANNER_FILE, YOUR_TELEGRAM_ID
from data.translations import (
    WELCOME, ABOUT, HELP, CONTACT_PROMPT, CONTACT_SENT,
    LANG_CHOICE, LANG_SELECTED, NO_ACCESS_CMD, ADMIN_REPLY_SENT,
    ADMIN_REPLY_FAIL, NO_USERNAME, UNKNOWN, NOT_RATED,
)
from keyboards.inline import (
    get_main_keyboard,
    get_contact_keyboard,
    get_stats_keyboard,
    get_contact_form_keyboard,
    get_lang_keyboard,
)
from utils import simulate_typing, is_user_rate_limited, safe_edit
from handlers.rating import track_user, load_stats, save_stats, get_lang, set_lang

router = Router()
logger = logging.getLogger(__name__)

_reply_map: dict[int, int] = {}


class ContactForm(StatesGroup):
    waiting_message = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state):
    user = message.from_user
    logger.info("User %s (@%s | ID: %s) started the bot", user.full_name, user.username, user.id)

    stats = load_stats()
    is_new_user = str(user.id) not in stats.get("users", {})

    track_user(user.id, user.full_name, user.username)

    if is_new_user and user.id != YOUR_TELEGRAM_ID:
        uname = f"@{user.username}" if user.username else "нет юзернейма"
        try:
            await message.bot.send_message(
                chat_id=YOUR_TELEGRAM_ID,
                text=(
                    f'<tg-emoji emoji-id="5258011929993026890">👤</tg-emoji> <b>Новый запуск!</b>\n\n'
                    f"Имя: <b>{user.full_name}</b>\n"
                    f"Юзер: {uname}\n"
                    f"ID: <code>{user.id}</code>"
                ),
            )
        except Exception as e:
            logger.warning("Failed to notify admin: %s", e)

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
        await message.answer(NO_ACCESS_CMD[get_lang(message.from_user.id)])
        return

    await _show_stats_page(message, page=1, lang=get_lang(message.from_user.id))


@router.callback_query(F.data.startswith("stats_page:"))
async def stats_page_callback(callback: CallbackQuery):
    if callback.from_user.id != YOUR_TELEGRAM_ID:
        await callback.answer(NO_ACCESS_CMD[get_lang(callback.from_user.id)], show_alert=True)
        return

    await callback.answer()
    try:
        page = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        return

    await _show_stats_page(callback.message, page, lang=get_lang(callback.from_user.id))


async def _show_stats_page(message, page: int, lang: str = "ru"):
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

    per_page = 5
    total_pages = max(1, (total_users + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))

    user_items = list(users.items())
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_users = user_items[start_idx:end_idx]

    header = (
        '<tg-emoji emoji-id="5231200819986047254">📊</tg-emoji> <b>Панель управления</b>\n\n'
        f'<tg-emoji emoji-id="5258513401784573443">👥</tg-emoji> Пользователей: <b>{total_users}</b> | '
        f'<tg-emoji emoji-id="5280881372418816002">👀</tg-emoji> Запусков: <b>{total_views}</b> | '
        f'<tg-emoji emoji-id="5258185631355378853">⭐</tg-emoji> Средняя: <b>{avg_rating:.1f}</b>\n\n'
        f"<b>Пользователи (стр. {page}/{total_pages}):</b>\n"
    )

    emojis = ["1\ufe0f\u20e3", "2\ufe0f\u20e3", "3\ufe0f\u20e3", "4\ufe0f\u20e3", "5\ufe0f\u20e3", "6\ufe0f\u20e3", "7\ufe0f\u20e3", "8\ufe0f\u20e3", "9\ufe0f\u20e3", "\U0001f51f"]

    lines = [header]
    for i, (uid, info) in enumerate(page_users):
        name = info.get("name", UNKNOWN[lang])
        uname = info.get("username")
        starts = info.get("starts", 0)
        last_seen = info.get("last_seen", "\u2014")
        tag = f"@{uname}" if uname else NO_USERNAME[lang]
        user_rating = rating_map.get(uid)
        rating_str = f'<tg-emoji emoji-id="5258185631355378853">⭐</tg-emoji> {user_rating}/5' if user_rating else NOT_RATED[lang]

        emoji = emojis[i] if i < len(emojis) else "\u25ab\ufe0f"
        lines.append(
            f"{emoji} <b>{name}</b> ({tag})\n"
            f'   <tg-emoji emoji-id="5372917041193828849">🚀</tg-emoji> {starts} запусков | <tg-emoji emoji-id="5967412305338568701">📅</tg-emoji> {last_seen}\n'
            f"   {rating_str}"
        )

    text = "\n\n".join(lines)
    keyboard = get_stats_keyboard(page, total_pages, lang)

    from utils import safe_edit
    await safe_edit(message, text=text, reply_markup=keyboard)


@router.callback_query(F.data == "show_about")
async def show_about(callback: CallbackQuery):
    await callback.answer()
    lang = get_lang(callback.from_user.id)
    await safe_edit(callback.message, text=ABOUT[lang], caption=ABOUT[lang], reply_markup=get_contact_keyboard(lang))


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
    await safe_edit(callback.message, text=CONTACT_PROMPT[lang], reply_markup=get_contact_form_keyboard(lang))


@router.message(ContactForm.waiting_message)
async def handle_contact_message(message: Message, state: FSMContext):
    await state.clear()

    user = message.from_user
    name = user.full_name
    lang = get_lang(user.id)
    uname = f"@{user.username}" if user.username else NO_USERNAME[lang]

    admin_text = (
        f'<tg-emoji emoji-id="5472239203590888751">📩</tg-emoji> <b>Новое сообщение от пользователя!</b>\n\n'
        f'<tg-emoji emoji-id="5258011929993026890">👤</tg-emoji> <b>{name}</b> ({uname})\n'
        f'<tg-emoji emoji-id="5936017305585586269">🆔</tg-emoji> ID: <code>{user.id}</code>\n\n'
        f'<tg-emoji emoji-id="5260535596941582167">💬</tg-emoji> {message.text}\n\n'
        f"<i>Ответьте на это сообщение, чтобы переслать ответ пользователю.</i>"
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
            text=f'<tg-emoji emoji-id="5472239203590888751">📩</tg-emoji> <b>Ответ от автора:</b>\n\n{message.text}',
        )
        lang = get_lang(user_id)
        await message.answer(ADMIN_REPLY_SENT[lang], reply_markup=get_main_keyboard(lang))
    except Exception as e:
        logger.error("Failed to forward reply to user %s: %s", user_id, e)
        await message.answer(ADMIN_REPLY_FAIL[lang], reply_markup=get_main_keyboard())


@router.callback_query(F.data == "noop")
async def noop_cb(callback: CallbackQuery):
    await callback.answer()
