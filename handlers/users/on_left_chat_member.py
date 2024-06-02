import logging

from aiogram import types
from aiogram.types.chat_member import ChatMemberStatus

from loader import dp
from database.methods.user_and_chat import delete


@dp.chat_member_handler(old_member_status=[
    ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER
], new_member_status=[ChatMemberStatus.BANNED, ChatMemberStatus.LEFT])
async def on_left_chat_member(chat_member: types.ChatMemberUpdated):
    chat_id = chat_member.chat.id
    member = chat_member.old_chat_member.user
    delete(member.id, chat_id)
    log_message = (
        f'A left (or kicked) user in a chat with id {chat_id}:\n'
        f'{member}'
    )
    logging.info(log_message)
