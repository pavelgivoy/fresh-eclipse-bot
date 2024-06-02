from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from parsers.guilds import parse_guild_roster
from database.methods.guild import get_by_name


class IsGuildRoster(BoundFilter):
    """This class checks that message contains a valid guild roster"""

    async def check(self, message: types.Message) -> bool:
        """Check that guild in the database and its roster is parsed successfully

        :param types.Message message: message with the guild roster
        :return bool: True if guild is found in the database and roster is parsed successfully, else False
        """
        guild_name, roster = parse_guild_roster(message.text)
        return roster and get_by_name(guild_name)
