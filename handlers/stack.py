import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.translations import STACK
from keyboards.inline import get_back_keyboard
from utils import safe_edit
from handlers.common import get_lang

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "show_stack")
async def show_stack(callback: CallbackQuery):
    await callback.answer()
    lang = get_lang(callback.from_user.id)
    await safe_edit(callback.message, text=STACK[lang], caption=STACK[lang], reply_markup=get_back_keyboard())
