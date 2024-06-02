from aiogram import types

from loader import dp
from database.methods import request
from utils.game_staff.answers import REQUEST_DELETED, REQUEST_ID_OR_TEXT_REQUIRED, REQUEST_NOT_FOUND


@dp.message_handler(commands=['del_wish'], chat_groups=['super'])
async def process_delete(message: types.Message):
    request_data = message.get_args()
    # argument with id or text of the request must be passed to get it
    if not request_data:
        await message.answer(REQUEST_ID_OR_TEXT_REQUIRED)
        return
    # id argument is passed
    elif request_data.isdigit():
        post = request.get(int(request_data))
    # id argument is not passed, filter by the given text
    else:
        post = request.get_by_text(request_data)

    if not post:
        await message.answer(REQUEST_NOT_FOUND)
        return

    request.delete(post)
    await message.answer(REQUEST_DELETED)
