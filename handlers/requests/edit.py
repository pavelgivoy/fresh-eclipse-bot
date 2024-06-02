from aiogram import types

from loader import dp
from database.methods.request import get, edit
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import REQUEST_ADDED, REQUEST_FOUND, REQUEST_ID_OR_TEXT_REQUIRED, REQUEST_ID_REQUIRED, REQUEST_NOT_FOUND


@dp.message_handler(commands=['edit_wish'], chat_groups=['super'])
async def process_add(message: types.Message):
    request_data = message.get_args()
    # If no text was found
    if not request_data:
        await message.answer(REQUEST_ID_OR_TEXT_REQUIRED)
        return

    request_data = request_data.split()
    if len(request_data) == 1:
        await message.answer(REQUEST_ID_OR_TEXT_REQUIRED)
        return

    request_id, text = request_data[0], request_data[1:]
    if not request_id.isdigit():
        await message.answer(REQUEST_ID_REQUIRED)
        return

    request = get(int(request_id))
    if not request:
        await message.answer(REQUEST_NOT_FOUND)
        return

    new_request_text = " ".join(text)
    if request.text == new_request_text:
        await message.answer(REQUEST_FOUND)
        return

    edit(request, new_request_text)
    await notify_admins(f'#хотелка\n{new_request_text}')
    await message.answer(REQUEST_ADDED)
