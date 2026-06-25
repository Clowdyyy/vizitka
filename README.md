# Telegram Bot - Portfolio

Interactive Telegram bot that showcases projects, tech stack, and contact info.

## Features

- Project carousel with navigation
- Tech stack display
- About me section
- Rating system (one vote per user)
- Admin stats panel (`/stats`)
- 24/7 deployment on Google Cloud

## Setup

1. Clone the repo:
```bash
git clone https://github.com/Clowdyyy/vizitka.git
cd vizitka
```

2. Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create `.env` file (use `.env.example` as template):
```bash
cp .env.example .env
```

4. Add your Bot Token (from @BotFather) and Telegram ID to `.env`

5. Run:
```bash
python bot.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Main menu |
| `/help` | Help info |
| `/stats` | Admin stats (owner only) |

## Project Structure

```
vizitka/
├── bot.py              # Entry point
├── config.py           # Configuration
├── utils.py            # Utilities
├── data/
│   └── projects.py     # Projects & text data
├── handlers/
│   ├── common.py       # /start, /help, /stats
│   ├── carousel.py     # Project carousel
│   ├── stack.py        # Tech stack
│   └── rating.py       # Rating & stats
├── keyboards/
│   └── inline.py       # All keyboards
└── assets/
    └── image_1.jpg     # Banner image
```

## License

MIT
