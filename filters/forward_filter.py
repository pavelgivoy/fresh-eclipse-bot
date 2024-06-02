from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class ForwardFilter(BoundFilter):
    """This filter checks that the message is forwarded from specified sources at specified time interval
    """

    def __init__(self, from_ids: list[int] | None = None, interval: int | None = None) -> None:
        self.from_ids = from_ids
        self.interval = interval
        # in some test cases forward time limits should be ignored
        self.TIMEOUT_ENABLED = False

    async def check(self, update: types.Message | types.CallbackQuery) -> bool:
        message = update if isinstance(
            update, types.Message) else update.message
        if not message.is_forward():
            return False
        if self.interval and self.TIMEOUT_ENABLED and datetime.timestamp(message.date) - datetime.timestamp(message.forward_date) > self.interval:
            return False
        forward_from = message.forward_from_chat if message.forward_from_chat and message.forward_from_chat.type == types.ChatType.CHANNEL else message.forward_from
        if self.from_ids and forward_from.id not in self.from_ids:
            return False
        return True
