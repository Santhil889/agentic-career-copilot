import logging
from typing import Any, Dict, Optional
import httpx
from app.config import settings

logger = logging.getLogger(__name__)


async def send_telegram_message(
    chat_id: Optional[str] = None,
    text: Optional[str] = None,
    parse_mode: str = "Markdown",
) -> Dict[str, Any]:
    """
    Sends a text message using the official Telegram Bot API:
    POST https://api.telegram.org/bot<token>/sendMessage
    """
    target_chat_id = chat_id or settings.TELEGRAM_CHAT_ID
    bot_token = settings.TELEGRAM_BOT_TOKEN

    if not bot_token or bot_token in {"your_bot_token_from_botfather", ""}:
        error_msg = "TELEGRAM_BOT_TOKEN is not configured in .env."
        logger.warning(error_msg)
        return {"ok": False, "description": error_msg}

    if not target_chat_id or target_chat_id in {"your_chat_id", ""}:
        error_msg = "Target chat_id is not provided and TELEGRAM_CHAT_ID is not configured in .env."
        logger.warning(error_msg)
        return {"ok": False, "description": error_msg}

    if not text:
        error_msg = "Message text cannot be empty."
        logger.warning(error_msg)
        return {"ok": False, "description": error_msg}

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": target_chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            data = response.json()

            if response.is_success and data.get("ok"):
                logger.info("Successfully sent Telegram message to chat_id=%s", target_chat_id)
                return data
            else:
                logger.error(
                    "Telegram API responded with error %s: %s",
                    response.status_code,
                    data.get("description", "Unknown error"),
                )
                return data
    except httpx.RequestError as exc:
        error_msg = f"Network/HTTP error while contacting Telegram API: {exc}"
        logger.exception(error_msg)
        return {"ok": False, "description": error_msg}
    except Exception as exc:
        error_msg = f"Unexpected error while sending Telegram message: {exc}"
        logger.exception(error_msg)
        return {"ok": False, "description": error_msg}
