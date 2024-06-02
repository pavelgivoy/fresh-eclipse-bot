import logging

from aiogram import types
from aiogram.types.chat_member import ChatMemberStatus

from loader import dp
from database.methods.user_and_chat import add_user


@dp.chat_member_handler(old_member_status=[ChatMemberStatus.BANNED, ChatMemberStatus.LEFT], new_member_status=ChatMemberStatus.MEMBER)
async def on_new_chat_member(chat_member: types.ChatMemberUpdated):
    chat_id = chat_member.chat.id
    member = chat_member.old_chat_member.user
    add_user(member.id, chat_id)
    log_message = (
        f'A new user in a chat with id {chat_id}:\n'
        f'{member}'
    )
    logging.info(log_message)
