from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes


def parse_allowed_ids(value: str | None) -> set[int]:
    if not value:
        return set()
    return {int(x) for x in value.split(",") if x.strip()}


def authorized(func):
    @wraps(func)
    async def wrapper(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        *args,
        **kwargs,
    ):
        user = update.effective_user
        chat = update.effective_chat
        allowed_users: set[int] = context.application.bot_data["allowed_user_ids"]
        allowed_chats: set[int] = context.application.bot_data["allowed_chat_ids"]

        if (user is None or user.id not in allowed_users) and (chat is None or chat.id not in allowed_chats):
            # Do not reveal anything to unauthorized users.
            return

        return await func(update, context, *args, **kwargs)

    return wrapper
