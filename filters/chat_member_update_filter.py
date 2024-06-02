from typing import Any, Dict, Union

from aiogram import types
from aiogram.types.chat_member import ChatMemberStatus
from aiogram.dispatcher.filters import Filter


MemberStatus = Union[*ChatMemberStatus.all()]


class ChatMemberUpdateFilter(Filter):
    """This filter checks that an user member status was updated from the old one to the new one
    """

    def __init__(self, old_member_status: MemberStatus | list[MemberStatus], new_member_status: MemberStatus | list[MemberStatus]) -> None:
        self.old_member_status = old_member_status if isinstance(
            old_member_status, list) else [old_member_status]
        self.new_member_status = new_member_status if isinstance(
            new_member_status, list) else [new_member_status]

    @classmethod
    def validate(cls, full_config: Dict[str, Any]) -> Dict[str, Any]:
        config = {}
        if 'old_member_status' in full_config:
            config['old_member_status'] = full_config.pop('old_member_status')
        if 'new_member_status' in full_config:
            config['new_member_status'] = full_config.pop('new_member_status')
        return config

    async def check(self, chat_member: types.ChatMemberUpdated) -> bool:
        return chat_member.old_chat_member.status in self.old_member_status \
            and chat_member.new_chat_member.status in self.new_member_status
