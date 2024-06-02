from aiogram import types

from utils.funcs.get_media import get_media
from loader import dp


@dp.message_handler(commands=['get_file_id'], user_groups=['super'])
async def get_file_id(message: types.Message):
    cur_instance = get_media(message.reply_to_message)
    file_id = cur_instance.file_id if cur_instance else None
    await message.answer(str(file_id))
