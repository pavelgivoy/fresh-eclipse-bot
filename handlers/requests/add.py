from aiogram import types

from loader import dp
from database.methods.request import add, get_by_text
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import REQUEST_ADDED, REQUEST_FOUND, REQUEST_NOT_DEFINED


@dp.message_handler(commands=['wish'], chat_groups=True)
async def process_add(message: types.Message):
    request_data = message.get_args()

    # text was not found
    if not request_data or len(request_data) <= 4:
        await message.answer(REQUEST_NOT_DEFINED)
        return

    # request with the given text found
    if get_by_text(request_data):
        await message.answer(REQUEST_FOUND)
        return

    add(request_data)
    await notify_admins(f'#хотелка\n{request_data}')
    await message.answer(REQUEST_ADDED)
