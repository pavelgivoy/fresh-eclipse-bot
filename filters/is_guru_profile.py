import re

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils.game_staff.regexps import ALCH_SPEC, BS_SPEC, FROM_CASTLE, GUILD_TAG_WITH_BRACKETS


class IsGuruProfile(BoundFilter):
    """This class checks that message contains a valid guru profile"""
    key = 'is_guru_profile'

    def __init__(self, is_guru_profile) -> None:
        self.is_guru_profile = is_guru_profile

    async def check(self, message: types.Message) -> bool:
        """Check that the message is guru profile

        :param types.Message message: message with the guru profile
        :return bool: True if guru profile is found, else False
        """
        if not self.is_guru_profile:
            return False
        text = message.text
        # a first line is the guru profile identifier
        first_line = re.match(
            r'^Добро пожаловать в .+ #\d{1,6}\.$', text, flags=re.MULTILINE)
        if not first_line:
            return False
        # each person has his castle
        castle = re.search(FROM_CASTLE, text, flags=re.MULTILINE)
        if not castle:
            return False
        else:
            castle = castle.group(1)
        # each guru has shop link
        link = re.search(r'/ws_[a-zA-Z0-9]{5}$', text, flags=re.MULTILINE)
        if not link:
            return False
        else:
            link = link.group(0)
        # next parameters are optional, but at least one guru spec must be defined
        guild = re.search(GUILD_TAG_WITH_BRACKETS, text, flags=re.MULTILINE)
        if guild:
            guild = guild.group(1)
        alch_spec = re.search(ALCH_SPEC, text, flags=re.MULTILINE)
        bs_spec = re.search(BS_SPEC, text, flags=re.MULTILINE)
        if not alch_spec and not bs_spec:
            return False
        if alch_spec:
            alch_spec = alch_spec.group(1)
        if bs_spec:
            bs_spec = bs_spec.group(1)

        return {
            'link': link,
            'castle': castle,
            'guild_tag': guild,
            'alch_spec': alch_spec,
            'bs_spec': bs_spec,
        }
