from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    from config import YOUR_TELEGRAM_ID
    lang_btn = "\U0001f310 \u042f\u0437\u044b\u043a" if lang == "ru" else "\U0001f310 Language"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\u2728 \u041c\u043e\u0438 \u043f\u0440\u043e\u0435\u043a\u0442\u044b" if lang == "ru" else "\u2728 Projects", callback_data="start_carousel")],
        [InlineKeyboardButton(text="\U0001f6e0\ufe0f \u0421\u0442\u0435\u043a" if lang == "ru" else "\U0001f6e0\ufe0f Stack", callback_data="show_stack")],
        [InlineKeyboardButton(text="\U0001f464 \u041e\u0431\u043e \u043c\u043d\u0435" if lang == "ru" else "\U0001f464 About", callback_data="show_about")],
        [InlineKeyboardButton(text="\u2709\ufe0f \u041d\u0430\u043f\u0438\u0441\u0430\u0442\u044c" if lang == "ru" else "\u2709\ufe0f Write", callback_data="write_to_author")],
        [InlineKeyboardButton(text="\U0001f4ca \u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430" if lang == "ru" else "\U0001f4ca Stats", callback_data="show_stats")],
        [InlineKeyboardButton(text=lang_btn, callback_data="change_lang")],
        [
            InlineKeyboardButton(text="GitHub", url="https://github.com/Clowdyyy"),
            InlineKeyboardButton(text="TikTok", url="https://www.tiktok.com/@clowdyxzz"),
        ],
    ])


def get_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\u2b05\ufe0f \u041d\u0430\u0437\u0430\u0434 \u0432 \u043c\u0435\u043d\u044e", callback_data="back_to_main")]
    ])


def get_carousel_keyboard(index: int) -> InlineKeyboardMarkup:
    from data.translations import PROJECTS
    total = len(PROJECTS["ru"])
    prev_idx = (index - 1) % total
    next_idx = (index + 1) % total

    buttons = [
        [
            InlineKeyboardButton(text="\u25c0\ufe0f", callback_data=f"carousel_goto:{prev_idx}"),
            InlineKeyboardButton(text=f"{index + 1} / {total}", callback_data="noop"),
            InlineKeyboardButton(text="\u25b6\ufe0f", callback_data=f"carousel_goto:{next_idx}"),
        ]
    ]

    buttons.append([
        InlineKeyboardButton(text="\U0001f451 \u041c\u0435\u043d\u044e", callback_data="back_to_main")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_contact_keyboard() -> InlineKeyboardMarkup:
    from config import YOUR_TELEGRAM_ID
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\U0001f4ac \u0412 \u043b\u0438\u0447\u043a\u0443", url=f"tg://user?id={YOUR_TELEGRAM_ID}")],
        [InlineKeyboardButton(text="\u2b50 \u041e\u0446\u0435\u043d\u0438\u0442\u044c", callback_data="show_rating")],
        [InlineKeyboardButton(text="\u2b05\ufe0f \u041d\u0430\u0437\u0430\u0434", callback_data="back_to_main")],
    ])


def get_contact_form_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\u2b05\ufe0f \u041e\u0442\u043c\u0435\u043d\u0430", callback_data="back_to_main")]
    ])


def get_stats_keyboard(page: int, total_pages: int) -> InlineKeyboardMarkup:
    buttons = []

    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="\u25c0\ufe0f", callback_data=f"stats_page:{page - 1}"))
    nav_row.append(InlineKeyboardButton(text=f"{page} / {total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="\u25b6\ufe0f", callback_data=f"stats_page:{page + 1}"))
    buttons.append(nav_row)

    buttons.append([InlineKeyboardButton(text="\u2b05\ufe0f \u041c\u0435\u043d\u044e", callback_data="back_to_main")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\U0001f1f7\U0001f1fa \u0420\u0443\u0441\u0441\u043a\u0438\u0439", callback_data="set_lang:ru")],
        [InlineKeyboardButton(text="\U0001f1ec\U0001f1e7 English", callback_data="set_lang:en")],
        [InlineKeyboardButton(text="\u2b05\ufe0f \u041d\u0430\u0437\u0430\u0434", callback_data="back_to_main")],
    ])


def get_rating_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 \u2b50", callback_data="rate:1"),
            InlineKeyboardButton(text="2 \u2b50", callback_data="rate:2"),
            InlineKeyboardButton(text="3 \u2b50", callback_data="rate:3"),
        ],
        [
            InlineKeyboardButton(text="4 \u2b50", callback_data="rate:4"),
            InlineKeyboardButton(text="5 \u2b50", callback_data="rate:5"),
        ],
        [InlineKeyboardButton(text="\u2b05\ufe0f \u041c\u0435\u043d\u044e", callback_data="back_to_main")],
    ])
