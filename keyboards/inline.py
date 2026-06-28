from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


BACK_RU = "⬅️ Назад в меню"
BACK_EN = "⬅️ Back to menu"
BACK_SHORT_RU = "⬅️ Назад"
BACK_SHORT_EN = "⬅️ Back"
MENU_RU = "👑 Меню"
MENU_EN = "👑 Menu"
CANCEL_RU = "⬅️ Отмена"
CANCEL_EN = "⬅️ Cancel"
DM_RU = "💬 В личку"
DM_EN = "💬 DM"
RATE_RU = "⭐ Оценить"
RATE_EN = "⭐ Rate"


def _back(lang):
    return BACK_RU if lang == "ru" else BACK_EN

def _back_short(lang):
    return BACK_SHORT_RU if lang == "ru" else BACK_SHORT_EN

def _menu(lang):
    return MENU_RU if lang == "ru" else MENU_EN


def get_main_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    from config import YOUR_TELEGRAM_ID
    lang_btn = "🌐 Язык" if lang == "ru" else "🌐 Language"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✨ Мои проекты" if lang == "ru" else "✨ Projects",
            callback_data="start_carousel",
            button_color="purple",
        )],
        [InlineKeyboardButton(
            text="🛠️ Стек" if lang == "ru" else "🛠️ Stack",
            callback_data="show_stack",
            button_color="orange",
        )],
        [InlineKeyboardButton(
            text="👤 Обо мне" if lang == "ru" else "👤 About",
            callback_data="show_about",
        )],
        [InlineKeyboardButton(
            text="✉️ Написать" if lang == "ru" else "✉️ Write",
            callback_data="write_to_author",
            button_color="green",
        )],
        [InlineKeyboardButton(
            text="📊 Статистика" if lang == "ru" else "📊 Stats",
            callback_data="show_stats",
            button_color="blue",
        )],
        [InlineKeyboardButton(text=lang_btn, callback_data="change_lang")],
        [
            InlineKeyboardButton(
                text="🌐 Сайт" if lang == "ru" else "🌐 Website",
                url="https://clowdy.is-a.dev/",
                button_color="blue",
            ),
        ],
        [
            InlineKeyboardButton(text="GitHub", url="https://github.com/Clowdyyy"),
            InlineKeyboardButton(text="TikTok", url="https://www.tiktok.com/@clowdyxzz"),
        ],
    ])


def get_back_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=_back(lang), callback_data="back_to_main")]
    ])


def get_carousel_keyboard(index: int) -> InlineKeyboardMarkup:
    from data.translations import PROJECTS
    total = len(PROJECTS["ru"])
    prev_idx = (index - 1) % total
    next_idx = (index + 1) % total

    buttons = [
        [
            InlineKeyboardButton(text="◀️", callback_data=f"carousel_goto:{prev_idx}"),
            InlineKeyboardButton(text=f"{index + 1} / {total}", callback_data="noop"),
            InlineKeyboardButton(text="▶️", callback_data=f"carousel_goto:{next_idx}"),
        ]
    ]

    buttons.append([
        InlineKeyboardButton(text=MENU_RU, callback_data="back_to_main")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_contact_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    from config import YOUR_TELEGRAM_ID
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=DM_RU if lang == "ru" else DM_EN, url=f"tg://user?id={YOUR_TELEGRAM_ID}")],
        [InlineKeyboardButton(text=RATE_RU if lang == "ru" else RATE_EN, callback_data="show_rating", button_color="yellow")],
        [InlineKeyboardButton(text=_back_short(lang), callback_data="back_to_main")],
    ])


def get_contact_form_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=CANCEL_RU if lang == "ru" else CANCEL_EN, callback_data="back_to_main")]
    ])


def get_stats_keyboard(page: int, total_pages: int, lang: str = "ru") -> InlineKeyboardMarkup:
    buttons = []

    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="◀️", callback_data=f"stats_page:{page - 1}"))
    nav_row.append(InlineKeyboardButton(text=f"{page} / {total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="▶️", callback_data=f"stats_page:{page + 1}"))
    buttons.append(nav_row)

    buttons.append([InlineKeyboardButton(text=_back_short(lang), callback_data="back_to_main")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang:en")],
        [InlineKeyboardButton(text=BACK_SHORT_RU, callback_data="back_to_main")],
    ])


def get_rating_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 ⭐", callback_data="rate:1"),
            InlineKeyboardButton(text="2 ⭐", callback_data="rate:2"),
            InlineKeyboardButton(text="3 ⭐", callback_data="rate:3"),
        ],
        [
            InlineKeyboardButton(text="4 ⭐", callback_data="rate:4"),
            InlineKeyboardButton(text="5 ⭐", callback_data="rate:5"),
        ],
        [InlineKeyboardButton(text=_back_short(lang), callback_data="back_to_main")],
    ])
