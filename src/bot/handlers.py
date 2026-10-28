from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, Application
from src.devices.base import Device
from src.services.status import get_all_statuses
from src.bot.security import authorized
import logging

logger = logging.getLogger(__name__)


async def _send_message(update: Update, text: str) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(text)
    else:
        logger.warning("No effective message")


@authorized
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await _send_message(
        update,
        "🎩 Salut! Moi c'est Alfred, votre assistant personnel.\n\n"
        "En quoi puis-je vous être utile aujourd'hui ?\n\n"
        "/clean — Démarre le robot aspirateur\n"
        "/feed — Distribue des croquettes\n",
    )


@authorized
async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    devices: list[Device] = context.application.bot_data["devices"]
    statuses = await get_all_statuses(devices)

    lines = ["Status\n"]

    for device in statuses:
        icon = "🟢" if device.available else "🔴"
        lines.append(f"{icon} {device.name}: {device.summary}")

    await _send_message(update, "\n".join(lines))


@authorized
async def clean(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await _send_message(update, "🧹 Le robot aspirateur n'est pas connecté.")


@authorized
async def feed(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await _send_message(update, "🍽️ Le distributeur de croquette n'est pas connecté.")


def register_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("clean", clean))
    application.add_handler(CommandHandler("feed", feed))
