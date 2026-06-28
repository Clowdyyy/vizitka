from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def _back(lang):
    return "Назад в меню" if lang == "ru" else "Back to menu"

def _back_short(lang):
    return "Назад" if lang == "ru" else "Back"


def get_main_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    from config import YOUR_TELEGRAM_ID
    lang_text = "Язык" if lang == "ru" else "Language"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Мои проекты" if lang == "ru" else "Projects",
            callback_data="start_carousel",
            icon_custom_emoji_id="5325547803936572038",
            button_color="primary",
        )],
        [InlineKeyboardButton(
            text="Стек" if lang == "ru" else "Stack",
            callback_data="show_stack",
            icon_custom_emoji_id="5988023995125993550",
            button_color="secondary",
        )],
        [InlineKeyboardButton(
            text="Обо мне" if lang == "ru" else "About",
            callback_data="show_about",
            icon_custom_emoji_id="5258011929993026890",
        )],
        [InlineKeyboardButton(
            text="Написать" if lang == "ru" else "Write",
            callback_data="write_to_author",
            icon_custom_emoji_id="5472239203590888751",
            button_color="primary",
        )],
        [InlineKeyboardButton(
            text="Статистика" if lang == "ru" else "Stats",
            callback_data="show_stats",
            icon_custom_emoji_id="5231200819986047254",
            button_color="secondary",
        )],
        [InlineKeyboardButton(
            text=lang_text,
            callback_data="change_lang",
            icon_custom_emoji_id="5256211458227715194",
        )],
        [
            InlineKeyboardButton(
                text="Сайт" if lang == "ru" else "Website",
                url="https://clowdy.is-a.dev/",
                icon_custom_emoji_id="5256211458227715194",
                button_color="primary",
            ),
        ],
        [
            InlineKeyboardButton(text="GitHub", url="https://github.com/Clowdyyy"),
            InlineKeyboardButton(text="TikTok", url="https://www.tiktok.com/@clowdyxzz"),
        ],
    ])


def get_back_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=_back(lang),
            callback_data="back_to_main",
            icon_custom_emoji_id="5258236805890710909",
        )]
    ])


def get_carousel_keyboard(index: int, lang: str = "ru") -> InlineKeyboardMarkup:
    from data.translations import PROJECTS
    total = len(PROJECTS["ru"])
    prev_idx = (index - 1) % total
    next_idx = (index + 1) % total

    buttons = [
        [
            InlineKeyboardButton(text="◀️", callback_data=f"carousel_goto:{prev_idx}", icon_custom_emoji_id="5256247952564825322"),
            InlineKeyboardButton(text=f"{index + 1} / {total}", callback_data="noop"),
            InlineKeyboardButton(text="▶️", callback_data=f"carousel_goto:{next_idx}", icon_custom_emoji_id="5255835489675519149"),
        ]
    ]

    buttons.append([
        InlineKeyboardButton(
            text="Меню" if lang == "ru" else "Menu",
            callback_data="back_to_main",
            icon_custom_emoji_id="5433758796289685818",
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_contact_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    from config import YOUR_TELEGRAM_ID
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="В личку" if lang == "ru" else "DM",
            url=f"tg://user?id={YOUR_TELEGRAM_ID}",
            icon_custom_emoji_id="5260535596941582167",
        )],
        [InlineKeyboardButton(
            text="Оценить" if lang == "ru" else "Rate",
            callback_data="show_rating",
            icon_custom_emoji_id="5258185631355378853",
            button_color="primary",
        )],
        [InlineKeyboardButton(
            text=_back_short(lang),
            callback_data="back_to_main",
            icon_custom_emoji_id="5258236805890710909",
        )],
    ])


def get_contact_form_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Отмена" if lang == "ru" else "Cancel",
            callback_data="back_to_main",
            icon_custom_emoji_id="5258236805890710909",
        )]
    ])


def get_stats_keyboard(page: int, total_pages: int, lang: str = "ru") -> InlineKeyboardMarkup:
    buttons = []

    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="◀️", callback_data=f"stats_page:{page - 1}", icon_custom_emoji_id="5256247952564825322"))
    nav_row.append(InlineKeyboardButton(text=f"{page} / {total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="▶️", callback_data=f"stats_page:{page + 1}", icon_custom_emoji_id="5255835489675519149"))
    buttons.append(nav_row)

    buttons.append([InlineKeyboardButton(
        text=_back_short(lang),
        callback_data="back_to_main",
        icon_custom_emoji_id="5258236805890710909",
    )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Русский",
            callback_data="set_lang:ru",
            icon_custom_emoji_id="5449408995691341691",
        )],
        [InlineKeyboardButton(
            text="English",
            callback_data="set_lang:en",
            icon_custom_emoji_id="5202196682497859879",
        )],
        [InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_main",
            icon_custom_emoji_id="5258236805890710909",
        )],
    ])


def get_rating_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="rate:1", icon_custom_emoji_id="5258185631355378853"),
            InlineKeyboardButton(text="2", callback_data="rate:2", icon_custom_emoji_id="5258185631355378853"),
            InlineKeyboardButton(text="3", callback_data="rate:3", icon_custom_emoji_id="5258185631355378853"),
        ],
        [
            InlineKeyboardButton(text="4", callback_data="rate:4", icon_custom_emoji_id="5258185631355378853"),
            InlineKeyboardButton(text="5", callback_data="rate:5", icon_custom_emoji_id="5258185631355378853"),
        ],
        [InlineKeyboardButton(
            text=_back_short(lang),
            callback_data="back_to_main",
            icon_custom_emoji_id="5258236805890710909",
        )],
    ])
