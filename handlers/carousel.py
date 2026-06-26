import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from data.projects import PROJECTS, LINE
from keyboards.inline import get_carousel_keyboard
from utils import safe_edit

router = Router()
logger = logging.getLogger(__name__)


class ProjectStates(StatesGroup):
    index = State()


def format_project(project: dict) -> str:
    stack_tags = " • ".join(f"<code>{s}</code>" for s in project["stack"])
    return (
        f"{LINE}\n"
        f"   {project['name']}\n"
        f"{LINE}\n\n"
        f"{project['desc']}\n\n"
        f"▸ Стек: {stack_tags}"
    )


@router.callback_query(F.data == "start_carousel")
async def start_carousel(callback: CallbackQuery, state):
    await callback.answer()
    await state.set_state(ProjectStates.index)
    await state.update_data(index=0)

    text = format_project(PROJECTS[0])
    await safe_edit(callback.message, text=text, caption=text, reply_markup=get_carousel_keyboard(0))


@router.callback_query(F.data.startswith("carousel_goto:"))
async def carousel_goto(callback: CallbackQuery, state):
    try:
        index = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.answer("Ошибка навигации", show_alert=True)
        return

    if index < 0 or index >= len(PROJECTS):
        await callback.answer("Проект не найден", show_alert=True)
        return

    await callback.answer()
    await state.update_data(index=index)

    text = format_project(PROJECTS[index])
    await safe_edit(callback.message, text=text, caption=text, reply_markup=get_carousel_keyboard(index))
