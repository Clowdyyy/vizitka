import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import get_back_keyboard
from utils import safe_edit

router = Router()
logger = logging.getLogger(__name__)

STACK_TEXT = (
    "🛠 <b>Мой технологический стек:</b>\n\n"
    "🌐 <b>Languages</b>\n"
    "    <code>Python</code>  <code>Java</code>\n\n"
    "🤖 <b>AI & RAG</b>\n"
    "    <code>LangChain</code>  <code>Google Gemini API</code>  <code>Ollama</code>\n\n"
    "⚡ <b>Frameworks</b>\n"
    "    <code>FastAPI</code>  <code>Aiogram 3</code>  <code>Streamlit</code>\n\n"
    "🗄 <b>Databases</b>\n"
    "    <code>PostgreSQL</code>  <code>ChromaDB</code>  <code>SQLite</code>\n\n"
    "🔧 <b>Tools</b>\n"
    "    <code>Git</code>  <code>GitHub</code>  <code>SQLAlchemy</code>"
)


@router.callback_query(F.data == "show_stack")
async def show_stack(callback: CallbackQuery):
    await callback.answer()
    await safe_edit(callback.message, text=STACK_TEXT, caption=STACK_TEXT, reply_markup=get_back_keyboard())
