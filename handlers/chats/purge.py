from aiogram import types

from loader import dp


@dp.message_handler(commands=['purge'], is_reply=True, user_groups=['super'])
async def purge_message(message: types.Message,
                        reply: types.Message):
    bot_member = await message.chat.get_member(message.bot.id)
    bot_is_admin = bot_member.is_chat_admin()
    bot_can_delete_messages = bot_is_admin and bot_member.can_delete_messages
    # message can be deleted if the bot is the message's creator
    # or maybe bot has privelleges to delete other users messages
    if bot_can_delete_messages or reply.from_user.id == message.bot.id:
        await reply.delete()
    # here it's obviously that bot is not message's creator
    if bot_can_delete_messages:
        await message.delete()
