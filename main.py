import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application
from src.devices import Robot, Feeder
from src.bot.handlers import register_handlers
from src.bot.security import parse_allowed_ids

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)


def main() -> None:
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing from .env")

    # create bot app
    application = Application.builder().token(token).build()

    # setup devices
    application.bot_data["devices"] = [Robot(), Feeder()]

    # setup allowed IDs
    allowed_user_ids = parse_allowed_ids(os.getenv("TELEGRAM_ALLOWED_USER_IDS", ""))
    allowed_chat_ids = parse_allowed_ids(os.getenv("TELEGRAM_ALLOWED_CHAT_IDS", ""))
    if not allowed_user_ids and not allowed_chat_ids:
        raise RuntimeError("TELEGRAM_ALLOWED_USER_IDS or TELEGRAM_ALLOWED_CHAT_IDS must contain at least one ID")
    application.bot_data["allowed_user_ids"] = allowed_user_ids
    application.bot_data["allowed_chat_ids"] = allowed_chat_ids

    # register handlers
    register_handlers(application)
    application.run_polling()


if __name__ == "__main__":
    main()
