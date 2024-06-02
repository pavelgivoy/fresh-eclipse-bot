import re

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsBattleOrder(BoundFilter):
    """This class checks that message contains a valid battle order"""
    key = 'is_battle_order'

    def __init__(self, is_battle_order) -> None:
        self.is_battle_order = is_battle_order

    async def check(self, message: types.Message) -> bool:
        """Check that guild in the database and its roster is parsed successfully

        :param types.Message message: message with the battle order
        :return bool: True if battle order is found, else False
        """
        if not self.is_battle_order:
            return False
        pinned_message = message.pinned_message
        date_regexp_check = re.match(
            r'^(?:01|09|17):00 \(\d{2}\.\d{2}\.\d{4}\)$', pinned_message.text, flags=re.MULTILINE)
        order_content_regexp_check = re.compile(
            r'^(?:(?:20\-40|40\-60|60\+) )?(?:🛡|⚔️)\S+ \S+(?: lvl\.\d{2})?$', flags=re.MULTILINE | re.UNICODE).search(pinned_message.text)
        return bool(date_regexp_check) and bool(order_content_regexp_check)
