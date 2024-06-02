import logging

from aiogram import types
from aiogram.types.chat_member import ChatMemberStatus

from loader import dp
from database.methods.user import update
from database.methods.user_and_chat import get
from filters.chat_member_update_filter import ChatMemberUpdateFilter
from utils.funcs.notify_admins import notify_admins


@dp.chat_member_handler(ChatMemberUpdateFilter(old_member_status=ChatMemberStatus.ADMINISTRATOR, new_member_status=[ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED]) | ChatMemberUpdateFilter(old_member_status=[ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED], new_member_status=ChatMemberStatus.ADMINISTRATOR))
@dp.my_chat_member_handler(ChatMemberUpdateFilter(old_member_status=ChatMemberStatus.ADMINISTRATOR, new_member_status=[ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED]) | ChatMemberUpdateFilter(old_member_status=[ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED], new_member_status=ChatMemberStatus.ADMINISTRATOR))
async def on_chat_admins_update(my_chat_member: types.ChatMemberUpdated):
    chat_id = my_chat_member.chat.id
    member = my_chat_member.old_chat_member.user
    user_id = member.id
    username = member.username
    user_and_chat = get(user_id, chat_id)
    user_and_chat.is_admin = not user_and_chat.is_admin
    update([user_and_chat])

    status_update_res = '' if user_and_chat.is_admin else ' не'

    ans = (
        f'Теперь пользователь <code>{user_id}</code> (@{username})'
        f'{status_update_res} является администратором чата <code>{chat_id}</code>'
    )
    await notify_admins(ans)
