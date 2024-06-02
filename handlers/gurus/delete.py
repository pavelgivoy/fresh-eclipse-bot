import re

from aiogram import types

from database.methods import master
from loader import dp
from utils.game_staff.answers import GURU_DELETED, GURU_NOT_FOUND, WRONG_SHOP_LINK
from utils.game_staff.basic_hq import BASIC_HQ_ID


@dp.message_handler(commands=['guru_delete'], chat_groups=['super', 'war', 'admin'], chat_alliances=[BASIC_HQ_ID])
async def start_process_guru_delete(message: types.Message):
    link = message.get_args()
    if not re.match(r'^/ws_[a-zA-Z0-9]{5}$', link):
        await message.answer(WRONG_SHOP_LINK)
        return
    delete_res = master.delete(link)
    if delete_res == 'not_found':
        await message.answer(GURU_NOT_FOUND)
    elif delete_res == 'deleted':
        await message.answer(GURU_DELETED)
