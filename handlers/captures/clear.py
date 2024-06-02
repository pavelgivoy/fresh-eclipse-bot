from aiogram import types

from loader import dp
from database.methods.captures import clear_locations
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import CLEAR_ALL_LOCATIONS_DONE, CLEAR_ALL_LOCATIONS_ERROR_DEV, CLEAR_ALL_LOCATIONS_ERROR_USER


@dp.message_handler(commands=['clear'], chat_groups=['super', 'war', 'admin'])
async def process_clear_locations(message: types.Message):
    res = clear_locations()
    if res == 'error':
        await notify_admins(CLEAR_ALL_LOCATIONS_ERROR_DEV)
        await message.answer(CLEAR_ALL_LOCATIONS_ERROR_USER)
    else:
        await message.answer(CLEAR_ALL_LOCATIONS_DONE)
