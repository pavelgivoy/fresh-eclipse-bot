from aiogram import types

from loader import dp


@dp.message_handler(commands=['bot_chat_member_info'], user_groups=['super'])
async def get_bot_chat_member_info(message: types.Message):
    bot_member = await message.chat.get_member(message.bot.id)
    await message.answer(str(bot_member))
