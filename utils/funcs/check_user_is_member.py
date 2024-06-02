from aiogram import types


async def check_user_is_member(message: types.Message, chat_id: int) -> bool:
    """Check if user is member of chat

    :param types.Message message: message which consists user that should be checked
    :param int chat_id: chat id which should be checked
    :return bool: True if user is member of chat, else False
    """
    member = await message.bot.get_chat_member(chat_id, message.from_user.id)
    return member.is_chat_member()
