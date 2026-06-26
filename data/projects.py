PROJECTS = [
    {
        "name": "AI DOCUMENT ANALYST",
        "desc": "Полностью локальная RAG-система для безопасного анализа PDF документов.",
        "stack": ["LangChain", "ChromaDB", "Ollama (Llama 3)", "Streamlit"],
        "github": None,
    },
    {
        "name": "AI TICKET AGENT",
        "desc": "ИИ-агент для автоматической обработки и классификации тикетов поддержки.",
        "stack": ["FastAPI", "Google Gemini API"],
        "github": None,
    },
    {
        "name": "NUTRIMIND BOT",
        "desc": "Telegram-бот для трекинга калорий и макронутриентов по текстовому описанию и фото еды.",
        "stack": ["Python", "Aiogram 3", "SQLAlchemy", "Gemini AI"],
        "github": None,
    },
    {
        "name": "PC CONTROL",
        "desc": "Telegram-бот для безопасного удалённого управления персональным компьютером.",
        "stack": ["Python", "Системные библиотеки"],
        "github": None,
    },
]

LINE = "━" * 24

WELCOME_TEXT = (
    f"{LINE}\n"
    "   ✦ АББОСХОН\n"
    "   Python Developer\n"
    f"{LINE}\n\n"
    "Привет! Я разработчик,\n"
    "создаю автоматизации,\n"
    "интегрирую ИИ-решения\n"
    "и пишу производительный код.\n\n"
    "▸ Добро пожаловать в моё\n"
    "  интерактивное портфолио."
)

ABOUT_TEXT = (
    f"{LINE}\n"
    "   ✦ ОБО МНЕ\n"
    f"{LINE}\n\n"
    "Я Аббосхон — Python-разработчик\n"
    "с фокусом на AI/ML и автоматизацию.\n\n"
    "▸ Создаю Telegram-ботов\n"
    "▸ Интегрирую LLM и RAG-системы\n"
    "▸ Пишу чистый, производительный код\n\n"
    "Напишите мне через кнопку ниже."
)

HELP_TEXT = (
    f"{LINE}\n"
    "   ✦ ПОМОЩЬ\n"
    f"{LINE}\n\n"
    "/start — Главное меню\n"
    "/help  — Эта справка\n\n"
    "Или просто нажимайте на кнопки."
)

STATS_TEXT = (
    f"{LINE}\n"
    "   ✦ СТАТИСТИКА\n"
    f"{LINE}\n\n"
    "Пользователей:  <b>{users}</b>\n"
    "Просмотров:     <b>{views}</b>\n"
    "Оценок:         <b>{ratings}</b>"
)

RATING_TEXT = (
    f"{LINE}\n"
    "   ✦ СПАСИБО ЗА ОЦЕНКУ\n"
    f"{LINE}\n\n"
    "Твоя оценка: {stars}\n\n"
    "Мне приятно, что тебе понравилось!"
)

CONTACT_PROMPT = (
    f"{LINE}\n"
    "   ✦ НАПИШИТЕ МНЕ\n"
    f"{LINE}\n\n"
    "Введите ваше сообщение\n"
    "и я отвечу вам."
)

CONTACT_SENT = (
    f"{LINE}\n"
    "   ✦ ОТПРАВЛЕНО\n"
    f"{LINE}\n\n"
    "Сообщение доставлено.\n"
    "Спасибо за обращение!"
)
