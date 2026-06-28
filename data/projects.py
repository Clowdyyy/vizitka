PROJECTS = [
    {
        "name": "AI DOCUMENT ANALYST",
        "emoji": '<tg-emoji emoji-id="6334809030518638180">💠</tg-emoji>',
        "desc": "Полностью локальная RAG-система для безопасного анализа PDF документов.",
        "stack": ["LangChain", "ChromaDB", "Ollama (Llama 3)", "Streamlit"],
        "github": None,
    },
    {
        "name": "AI TICKET AGENT",
        "emoji": '<tg-emoji emoji-id="5807465992363710697">💎</tg-emoji>',
        "desc": "ИИ-агент для автоматической обработки и классификации тикетов поддержки.",
        "stack": ["FastAPI", "Google Gemini API"],
        "github": None,
    },
    {
        "name": "NUTRIMIND BOT",
        "emoji": '<tg-emoji emoji-id="5935989710420709120">🍎</tg-emoji>',
        "desc": "Многофункциональный Telegram-бот для удобного трекинга калорий и макронутриентов по текстовому описанию и фото еды.",
        "stack": ["Python", "Aiogram 3", "SQLAlchemy", "Gemini AI"],
        "github": None,
    },
    {
        "name": "PC CONTROL",
        "emoji": '<tg-emoji emoji-id="5879609898064415920">💻</tg-emoji>',
        "desc": "Telegram-бот для безопасного удаленного управления персональным компьютером.",
        "stack": ["Python", "Системные библиотеки"],
        "github": None,
    },
]

WELCOME_TEXT = (
    '<tg-emoji emoji-id="5458904472598095631">👋</tg-emoji> Привет! Меня зовут <b>Аббосхон</b>.\n\n'
    '<tg-emoji emoji-id="5372917041193828849">🚀</tg-emoji> Я разработчик, создаю автоматизации, интегрирую ИИ-решения и пишу производительный код.\n\n'
    "<i>Добро пожаловать в мое интерактивное портфолио! Выберите интересующий раздел:</i>"
)

ABOUT_TEXT = (
    '<tg-emoji emoji-id="5258011929993026890">👤</tg-emoji> <b>Обо мне</b>\n\n'
    "Привет! Я <b>Аббосхон</b> — Python-разработчик с фокусом на AI/ML и автоматизацию.\n\n"
    '<tg-emoji emoji-id="5296376222853377734">🔹</tg-emoji> Создаю умных Telegram-ботов\n'
    '<tg-emoji emoji-id="5296376222853377734">🔹</tg-emoji> Интегрирую LLM и RAG-системы\n'
    '<tg-emoji emoji-id="5296376222853377734">🔹</tg-emoji> Пишу чистый, производительный код\n\n'
    '<tg-emoji emoji-id="5472239203590888751">📩</tg-emoji> Связаться со мной можно через кнопку ниже!'
)

HELP_TEXT = (
    '<tg-emoji emoji-id="5382187118216879236">❓</tg-emoji> <b>Как пользоваться ботом</b>\n\n'
    '<tg-emoji emoji-id="5258461531464539536">📌</tg-emoji> <b>/start</b> — Главное меню\n'
    '<tg-emoji emoji-id="5258461531464539536">📌</tg-emoji> <b>/help</b> — Эта справка\n\n'
    'Или просто нажимайте на кнопки в меню! <tg-emoji emoji-id="5231102735817918643">👇</tg-emoji>'
)

STATS_TEXT = (
    '<tg-emoji emoji-id="5231200819986047254">📊</tg-emoji> <b>Статистика бота</b>\n\n'
    '<tg-emoji emoji-id="5258513401784573443">👥</tg-emoji> Пользователей: <b>{users}</b>\n'
    '<tg-emoji emoji-id="5280881372418816002">👀</tg-emoji> Просмотров портфолио: <b>{views}</b>\n'
    '<tg-emoji emoji-id="5260535596941582167">💬</tg-emoji> Оценок: <b>{ratings}</b>'
)

RATING_TEXT = (
    '<tg-emoji emoji-id="5258185631355378853">⭐</tg-emoji> <b>Спасибо за оценку!</b>\n\n'
    "Твоя оценка: {stars}\n\n"
    "Мне приятно, что тебе понравилось!"
)

CONTACT_PROMPT = '<tg-emoji emoji-id="5877214659227946561">✍️</tg-emoji> <b>Напишите ваше сообщение:</b>\n\nЯ его получу и отвечу вам как смогу!'

CONTACT_SENT = '<tg-emoji emoji-id="5260416304224936047">✅</tg-emoji> <b>Сообщение отправлено!</b>\n\nСпасибо за обращение!'
