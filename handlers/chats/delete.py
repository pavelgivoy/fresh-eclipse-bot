from aiogram import types

from loader import dp
from database.methods import chat
from parsers.chats import parse_chat_id_info
from utils.game_staff.answers import CHAT_DELETED, CHAT_DELETING_ERROR_DEV, CHAT_UNKNOWN, NO_CHAT_ID


@dp.message_handler(commands=['delete_chat'], chat_groups=['super'])
async def process_delete(message: types.Message):
    chat_id = parse_chat_id_info(message)

    if not chat_id:
        await message.answer(NO_CHAT_ID)
        return

    found_chat = chat.get_chat_from_group_chat_id(chat_id)

    if found_chat is None:
        await message.answer(CHAT_UNKNOWN.format(str(chat_id)))
        return

    delete_res = chat.delete(found_chat)
    if delete_res == 'error':
        await message.answer(CHAT_DELETING_ERROR_DEV)
    else:
        await message.answer(CHAT_DELETED)
