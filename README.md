# Telegram Reminder Bot (V0)

A lightweight, deterministic FastAPI backend that sends daily Telegram reminders to update your Naukri profile, with incoming webhook support and APScheduler.

## Quick Start

### 1. Set Up Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Credentials

Copy `.env.example` to `.env` and fill in your details:

```bash
cp .env.example .env
```

Edit `.env`:
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
TELEGRAM_CHAT_ID=987654321
REMINDER_HOUR=9
REMINDER_MINUTE=0
TIMEZONE=Asia/Kolkata
```

### 3. Run the Server

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### 4. Live Cloud Production (Render)

- **Live URL**: [https://agentic-career-copilot.onrender.com](https://agentic-career-copilot.onrender.com)
- **Health Check**: [https://agentic-career-copilot.onrender.com/health](https://agentic-career-copilot.onrender.com/health)
- **Interactive Swagger Docs**: [https://agentic-career-copilot.onrender.com/docs](https://agentic-career-copilot.onrender.com/docs)
- **Active Webhook**: `https://agentic-career-copilot.onrender.com/webhook/telegram`

### 5. Running Tests

```bash
source .venv/bin/activate
pytest
```
