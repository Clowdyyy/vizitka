from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.projects import PROJECTS


def get_main_keyboard() -> InlineKeyboardMarkup:
    from config import YOUR_TELEGRAM_ID
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Проекты", callback_data="start_carousel")],
        [InlineKeyboardButton(text="Стек", callback_data="show_stack")],
        [InlineKeyboardButton(text="Обо мне", callback_data="show_about")],
        [InlineKeyboardButton(text="Написать мне", callback_data="write_to_author")],
        [InlineKeyboardButton(text="Статистика", callback_data="show_stats")],
        [
            InlineKeyboardButton(text="GitHub", url="https://github.com/Clowdyyy"),
            InlineKeyboardButton(text="TikTok", url="https://www.tiktok.com/@clowdyxzz"),
        ],
    ])


def get_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_main")]
    ])


def get_carousel_keyboard(index: int) -> InlineKeyboardMarkup:
    total = len(PROJECTS)
    prev_idx = (index - 1) % total
    next_idx = (index + 1) % total
    project = PROJECTS[index]

    buttons = [
        [
            InlineKeyboardButton(text="◀", callback_data=f"carousel_goto:{prev_idx}"),
            InlineKeyboardButton(text=f"{index + 1} / {total}", callback_data="noop"),
            InlineKeyboardButton(text="▶", callback_data=f"carousel_goto:{next_idx}"),
        ]
    ]

    if project.get("github"):
        buttons.append([
            InlineKeyboardButton(text="Репозиторий", url=project["github"])
        ])

    buttons.append([
        InlineKeyboardButton(text="← Меню", callback_data="back_to_main")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_contact_keyboard() -> InlineKeyboardMarkup:
    from config import YOUR_TELEGRAM_ID
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Написать в личку", url=f"tg://user?id={YOUR_TELEGRAM_ID}")],
        [InlineKeyboardButton(text="Оценить бота", callback_data="show_rating")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_main")],
    ])


def get_contact_form_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Отмена", callback_data="back_to_main")]
    ])


def get_stats_keyboard(page: int, total_pages: int) -> InlineKeyboardMarkup:
    buttons = []

    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="◀", callback_data=f"stats_page:{page - 1}"))
    nav_row.append(InlineKeyboardButton(text=f"{page} / {total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="▶", callback_data=f"stats_page:{page + 1}"))
    buttons.append(nav_row)

    buttons.append([InlineKeyboardButton(text="← Меню", callback_data="back_to_main")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_rating_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1 ★", callback_data="rate:1"),
            InlineKeyboardButton(text="2 ★", callback_data="rate:2"),
            InlineKeyboardButton(text="3 ★", callback_data="rate:3"),
        ],
        [
            InlineKeyboardButton(text="4 ★", callback_data="rate:4"),
            InlineKeyboardButton(text="5 ★", callback_data="rate:5"),
        ],
        [InlineKeyboardButton(text="← Меню", callback_data="back_to_main")],
    ])
