import json
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.config import settings
from app.scheduler import setup_scheduler, send_daily_naukri_reminder

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("telegram_bot_backend")

# Initialize scheduler
scheduler = setup_scheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan context manager:
    - Starts the APScheduler when the application starts up.
    - Shuts down the scheduler cleanly when the application terminates.
    """
    logger.info("Starting up Telegram Reminder Bot backend...")
    scheduler.start()
    logger.info("APScheduler started successfully.")
    yield
    logger.info("Shutting down APScheduler...")
    scheduler.shutdown(wait=False)
    logger.info("Application shutdown complete.")


app = FastAPI(
    title="Telegram Reminder Bot Backend",
    description="V0 deterministic backend with FastAPI, APScheduler, and Telegram Webhook integration.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", tags=["General"])
async def root():
    return {
        "service": "Telegram Reminder Bot Backend",
        "version": "0.1.0",
        "status": "online",
        "docs_url": "/docs",
    }


@app.get("/health", tags=["General"])
async def health_check():
    """
    Returns the server health and next scheduled reminder time.
    """
    job = scheduler.get_job("naukri_reminder_job")
    next_run = "Pending scheduler start"
    if job and hasattr(job, "next_run_time") and job.next_run_time:
        next_run = str(job.next_run_time)

    return {
        "status": "healthy",
        "scheduler_running": scheduler.running,
        "is_configured": settings.is_configured,
        "reminder_schedule": {
            "cron_hours": settings.cron_hour_expression,
            "minute": settings.REMINDER_MINUTE,
            "interval_hours": settings.REMINDER_INTERVAL_HOURS,
            "start_hour": settings.REMINDER_START_HOUR,
            "end_hour": settings.REMINDER_END_HOUR,
            "timezone": settings.TIMEZONE,
            "next_run_time": next_run,
        },
    }


@app.post("/webhook/telegram", tags=["Telegram Webhook"])
async def telegram_webhook(request: Request):
    """
    Receives incoming Telegram updates via Webhook.
    Acknowledges receipt immediately with HTTP 200 and logs/prints the payload.
    """
    try:
        payload: Dict[str, Any] = await request.json()
    except Exception:
        payload = {}

    # Pretty-print incoming update to console
    print("\n" + "=" * 50)
    print("📩 [INCOMING TELEGRAM WEBHOOK MESSAGE]")
    print(json.dumps(payload, indent=2))
    print("=" * 50 + "\n")

    # Extract high-level information if this is a standard message
    message = payload.get("message") or payload.get("edited_message")
    if message:
        from_user = message.get("from", {})
        sender_name = from_user.get("first_name", "Unknown")
        sender_id = from_user.get("id")
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "<non-text message>")

        logger.info(
            "Received message from %s (user_id=%s, chat_id=%s): '%s'",
            sender_name,
            sender_id,
            chat_id,
            text,
        )

    # Return HTTP 200 OK to Telegram so it doesn't retry the delivery
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ok", "received": True},
    )


@app.post("/test-reminder", tags=["Manual Testing"])
async def trigger_manual_reminder():
    """
    Manually triggers the daily reminder message right now.
    Useful for testing Telegram delivery without waiting for the scheduled cron time.
    """
    logger.info("Manual test reminder requested via /test-reminder")
    result = await send_daily_naukri_reminder()
    return {
        "status": "triggered",
        "telegram_response": result,
    }
