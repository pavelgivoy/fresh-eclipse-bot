from aiogram import types

from loader import dp


@dp.message_handler(commands=['dump'], is_reply=True, user_groups=['super'])
async def show_full_message_info(message: types.Message):
    await message.answer(str(message.reply_to_message))
