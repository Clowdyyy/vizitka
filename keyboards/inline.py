from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.projects import PROJECTS


def get_main_keyboard() -> InlineKeyboardMarkup:
    from config import YOUR_TELEGRAM_ID
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✨ Мои проекты", callback_data="start_carousel")],
        [InlineKeyboardButton(text="🛠 Мой стек технологий", callback_data="show_stack")],
        [InlineKeyboardButton(text="👤 Обо мне", callback_data="show_about")],
        [InlineKeyboardButton(text="✉️ Написать в личку", url=f"tg://user?id={YOUR_TELEGRAM_ID}")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="show_stats")],
    ])


def get_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_main")]
    ])


def get_carousel_keyboard(index: int) -> InlineKeyboardMarkup:
    total = len(PROJECTS)
    prev_idx = (index - 1) % total
    next_idx = (index + 1) % total
    project = PROJECTS[index]

    buttons = [
        [
            InlineKeyboardButton(text="◀️", callback_data=f"carousel_goto:{prev_idx}"),
            InlineKeyboardButton(text=f"▫️ {index + 1} / {total} ▫️", callback_data="noop"),
            InlineKeyboardButton(text="▶️", callback_data=f"carousel_goto:{next_idx}"),
        ]
    ]

    if project.get("github"):
        buttons.append([
            InlineKeyboardButton(text="🔗 Репозиторий", url=project["github"])
        ])

    buttons.append([
        InlineKeyboardButton(text="👑 Главное Меню", callback_data="back_to_main")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_contact_keyboard() -> InlineKeyboardMarkup:
    from config import YOUR_TELEGRAM_ID
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Написать в личку", url=f"tg://user?id={YOUR_TELEGRAM_ID}")],
        [InlineKeyboardButton(text="⭐ Оценить бота", callback_data="show_rating")],
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_main")],
    ])


def get_rating_keyboard() -> InlineKeyboardMarkup:
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
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_main")],
    ])
