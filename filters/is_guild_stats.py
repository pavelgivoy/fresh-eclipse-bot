from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from database.methods.guild import get_all


class IsGuildStats(BoundFilter):
    """This class checks that message contains a guild stats"""

    async def check(self, message: types.Message) -> bool:
        """Check that guild in the database

        :param types.Message message: message with the guild stats
        :return bool: True if guild is found in the database and message contains guild stats, else False
        """
        first_line = message.text.splitlines()[0]
        if 'Attack Rating' not in first_line and 'Defence Rating' not in first_line:
            return False
        guilds = get_all()
        for guild in guilds:
            if guild.name in first_line:
                return True
        return False
