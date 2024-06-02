import logging
from aiogram import types
from aiogram.types.chat_member import ChatMemberStatus

from loader import dp
from database.methods import chat
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import BOT_LEFT_THE_CHAT


@dp.my_chat_member_handler(old_member_status=[
    ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED
], new_member_status=[ChatMemberStatus.KICKED, ChatMemberStatus.LEFT])
async def on_exit_chat(my_chat_member: types.ChatMemberUpdated):
    logging.info('Process my chat member update')
    chat_id = my_chat_member.chat.id
    found_chat = chat.get_chat_from_group_chat_id(chat_id)

    if found_chat is not None:
        chat.delete(found_chat)
        await notify_admins(BOT_LEFT_THE_CHAT.format(str(chat_id)))
