# Bounty Sniper Bot

An asynchronous Telegram bot that monitors GitHub for open Python bounty issues and sends new matches directly to a Telegram chat. Built with Python 3.12, `asyncio`, aiogram 3, `aiohttp`, and the GitHub Issues API.

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3-2CA5E0?logo=telegram&logoColor=white)](https://docs.aiogram.dev/)

## Features

- Asynchronously polls GitHub for open, public issues labeled `bounty` in Python repositories.
- Filters configured repositories and keywords to remove unwanted results.
- Sends newly discovered issues to Telegram, with duplicate suppression while the bot is running.
- Runs periodic checks every five minutes and supports starting and stopping monitoring from the Telegram chat.
- Uses the GitHub Issues Search API; an optional GitHub token can be configured to increase API rate limits.

## Setup

### Prerequisites

- Python 3.12
- A Telegram bot token, created with [@BotFather](https://t.me/BotFather)
- A Telegram account to start and control the bot

### Install

Clone the repository and enter its directory:

```bash
git clone https://github.com/frankoffhotels-cmd/bounty-sniper-bot.git
cd bounty-sniper-bot
```

Create and activate a virtual environment:

**Windows (PowerShell):**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### Configure environment

Create a `.env` file in the project root:

```dotenv
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GITHUB_TOKEN=your_github_personal_access_token
```

`TELEGRAM_BOT_TOKEN` is required. `GITHUB_TOKEN` is optional, but recommended to benefit from higher GitHub API rate limits. Keep credentials private; do not commit `.env` to version control.

### Run

Start the bot:

```bash
python main.py
```

Open the bot in Telegram, send `/start`, and use **▶️ Поиск Bounty** to begin monitoring. Use **⏹ Стоп** to stop it.

## Architecture

- **`scraper.py`** — asynchronously queries GitHub's Issues Search API with `aiohttp`, validates the response, and filters results by repository and title.
- **`main.py`** — loads configuration from `.env`, registers Telegram commands and keyboard handlers with aiogram, and manages the asynchronous monitoring loop, duplicate suppression, and notifications.
