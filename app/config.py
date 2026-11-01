from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Telegram credentials
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    # Daily reminder cron schedule
    REMINDER_HOUR: int = 9
    REMINDER_MINUTE: int = 0
    TIMEZONE: str = "Asia/Kolkata"

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
