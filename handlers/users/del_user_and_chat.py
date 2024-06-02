from aiogram import types

from loader import dp
from database.methods import user_and_chat
from parsers.users import parse_user_and_chat
from utils.game_staff.answers import USER_ID_REQUIRED


@dp.message_handler(commands=['del_user_and_chat'],
                    user_groups=['super'])
async def process_del_user_and_chat(message: types.Message):
    args = message.get_args().split()
    chat_id, user_id = parse_user_and_chat(args)
    if not user_id:
        await message.answer(USER_ID_REQUIRED)
        return
    if not chat_id:
        chat_id = message.chat.id

    delete_res = user_and_chat.delete(user_id, chat_id)
    if delete_res == 'error':
        await message.answer('Нет такой записи')
        return
    await message.answer('Ok')
