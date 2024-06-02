from aiogram import types

from loader import dp
from utils.funcs.notify_admins import notify_admins


@dp.message_handler(commands=['leave_chat'], chat_groups=['super'])
async def leave_chat(message: types.Message):
    chat_id = int(message.get_args())
    try:
        await message.bot.leave_chat(chat_id)
    except Exception as e:
        await notify_admins(str(e))
    else:
        await message.answer('Done')
