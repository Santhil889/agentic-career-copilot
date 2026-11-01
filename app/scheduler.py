import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config import settings
from app.telegram import send_telegram_message

logger = logging.getLogger(__name__)

# Daily reminder message template
NAUKRI_REMINDER_TEXT = (
    "🔔 *Daily Naukri Profile Reminder*\n\n"
    "Hey! Just a reminder to take 2 minutes and update your Naukri profile today:\n\n"
    "• Update your resume headline or key skills\n"
    "• Refresh your profile to appear at the top of recruiter searches\n"
    "• Review any new recruiter views or job alerts\n\n"
    "👉 [Open Naukri Profile](https://www.naukri.com/mnjuser/profile)\n"
    "_Consistency in profile activity boosts recruiter visibility!_ 🚀"
)


async def send_daily_naukri_reminder() -> dict:
    """
    Job triggered by APScheduler every day to send the Naukri reminder message.
    """
    logger.info("Executing daily Naukri profile reminder task...")
    result = await send_telegram_message(
        chat_id=settings.TELEGRAM_CHAT_ID,
        text=NAUKRI_REMINDER_TEXT,
    )
    return result


def setup_scheduler() -> AsyncIOScheduler:
    """
    Configures and returns an AsyncIOScheduler instance with the daily cron trigger.
    """
    scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)

    trigger = CronTrigger(
        hour=settings.cron_hour_expression,
        minute=settings.REMINDER_MINUTE,
        timezone=settings.TIMEZONE,
    )

    scheduler.add_job(
        send_daily_naukri_reminder,
        trigger=trigger,
        id="naukri_reminder_job",
        name="Naukri Profile Reminder Job",
        replace_existing=True,
    )

    logger.info(
        "Configured reminder job with hours='%s', minute=%02d (%s)",
        settings.cron_hour_expression,
        settings.REMINDER_MINUTE,
        settings.TIMEZONE,
    )

    return scheduler
