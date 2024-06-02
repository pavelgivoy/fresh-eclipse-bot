from aiogram import types

from database.methods.chat import get_chat_from_group_chat_id
from loader import dp


@dp.message_handler(commands=['get_group'], user_groups=['super'])
async def get_chat_group(message: types.Message):
    chat = get_chat_from_group_chat_id(message.chat.id)
    group = chat.group if chat else 'not allowed'
    await message.answer(group)
