# Bounty Sniper Bot 🎯

An asynchronous Telegram bot that aggregates open-source bounty tasks from GitHub API and sends real-time notifications.

## Technology Stack

- Python 3.12
- aiogram 3
- aiohttp
- python-dotenv

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<your-repository>.git
   cd <your-repository>
   ```

2. Create and activate a virtual environment:

   **Windows (PowerShell):**

   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and configure your credentials:

   ```dotenv
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   GITHUB_TOKEN=your_github_token
   ```

   Keep `.env` private. It is excluded from version control by `.gitignore`.

5. Start the bot:

   ```bash
   python main.py
   ```

Created as a portfolio project to automate the search for open-source bounties.
