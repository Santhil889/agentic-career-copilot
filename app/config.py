from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Telegram credentials
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    # Reminder schedule configuration
    # Default: Every 2 hours between 09:00 and 22:00 IST
    REMINDER_INTERVAL_HOURS: int = 2
    REMINDER_START_HOUR: int = 9
    REMINDER_END_HOUR: int = 22
    REMINDER_MINUTE: int = 0
    REMINDER_CRON_HOUR: str = ""
    TIMEZONE: str = "Asia/Kolkata"

    @property
    def cron_hour_expression(self) -> str:
        """Computes the cron hour expression (e.g., '9-22/2' or '*/2')."""
        if self.REMINDER_CRON_HOUR:
            return self.REMINDER_CRON_HOUR
        if self.REMINDER_START_HOUR == 0 and self.REMINDER_END_HOUR >= 23:
            return f"*/{self.REMINDER_INTERVAL_HOURS}"
        return f"{self.REMINDER_START_HOUR}-{self.REMINDER_END_HOUR}/{self.REMINDER_INTERVAL_HOURS}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def is_configured(self) -> bool:
        """Check if essential credentials are set and not placeholder values."""
        placeholder_tokens = {"", "your_bot_token_from_botfather", "your_token"}
        placeholder_chats = {"", "your_chat_id", "your_chat_id_here"}
        return (
            self.TELEGRAM_BOT_TOKEN not in placeholder_tokens
            and self.TELEGRAM_CHAT_ID not in placeholder_chats
        )


settings = Settings()
