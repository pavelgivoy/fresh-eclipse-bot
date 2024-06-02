from aiogram import types

from loader import dp
from database.methods import chat


@dp.message_handler(commands=['list_chats'], chat_groups=['super'])
async def process_show_chats(message: types.Message):
    ans = '[' + ',\n'.join(list(map(str, chat.get_all()))) + ']'

    await message.answer(ans)
