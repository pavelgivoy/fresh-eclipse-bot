from database.methods.chat import get_all
from loader import bot


async def notify_admins(text: str,
                        groups: list[str] | None = None):
    """Send notification about some important things into admin chats

    :param str text: notification text
    :param list[str] groups: chat groups where the message should be sent, defaults to None (message will be sent to chats of super group only)
    """
    groups = groups or ['super']
    chats = get_all(groups=groups)

    for chat in chats:
        await bot.send_message(chat_id=chat.id, text=text)
