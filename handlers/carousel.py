import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from data.translations import PROJECTS
from data.projects import PROJECTS as OldProjects
from keyboards.inline import get_carousel_keyboard
from utils import safe_edit
from handlers.rating import get_lang

router = Router()
logger = logging.getLogger(__name__)


class ProjectStates(StatesGroup):
    index = State()


def format_project(project: dict) -> str:
    stack_tags = " ".join(f"<code>{s}</code>" for s in project["stack"])
    emoji = project.get("emoji", "")
    prefix = f"{emoji} " if emoji else ""
    return (
        f"{prefix}<b>{project['name']}</b>\n\n"
        f"{project['desc']}\n\n"
        f"\u2699\ufe0f <b>\u0421\u0442\u0435\u043a:</b> {stack_tags}"
    )


@router.callback_query(F.data == "start_carousel")
async def start_carousel(callback: CallbackQuery, state):
    await callback.answer()
    await state.set_state(ProjectStates.index)
    await state.update_data(index=0)

    lang = get_lang(callback.from_user.id)
    projects = PROJECTS.get(lang, OldProjects)
    text = format_project(projects[0])
    await safe_edit(callback.message, text=text, caption=text, reply_markup=get_carousel_keyboard(0))


@router.callback_query(F.data.startswith("carousel_goto:"))
async def carousel_goto(callback: CallbackQuery, state):
    try:
        index = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.answer("\u041e\u0448\u0438\u0431\u043a\u0430 \u043d\u0430\u0432\u0438\u0433\u0430\u0446\u0438\u0438", show_alert=True)
        return

    lang = get_lang(callback.from_user.id)
    projects = PROJECTS.get(lang, OldProjects)

    if index < 0 or index >= len(projects):
        await callback.answer("\u041f\u0440\u043e\u0435\u043a\u0442 \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d", show_alert=True)
        return

    await callback.answer()
    await state.update_data(index=index)

    text = format_project(projects[index])
    await safe_edit(callback.message, text=text, caption=text, reply_markup=get_carousel_keyboard(index))
