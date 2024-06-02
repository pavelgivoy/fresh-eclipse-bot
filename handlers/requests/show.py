from aiogram import types

from loader import dp
from database.methods.request import get_all, get
from utils.game_staff.answers import REQUEST_NOT_FOUND


@dp.message_handler(commands=['show_wishes'], chat_groups=['super'])
async def process_show_request(message: types.Message):
    request_data = message.get_args()

    # if id argument is not passed, show all known requests
    if not request_data:
        ans = '[' + ',\n'.join(list(map(str, get_all()))) + ']'
        await message.answer(ans)
        return

    request = get(int(request_data))
    if not request:
        await message.answer(REQUEST_NOT_FOUND)
        return

    await message.answer(request.text)
