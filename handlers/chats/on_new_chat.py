from aiogram import types
from aiogram.types.chat_member import ChatMemberStatus

from loader import dp, bot
from database.methods.chat import get_chat_from_group_chat_id
from database.methods.user_and_chat import add_admins
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import UNKNOWN_CHAT_WARNING_DEV, UNKNOWN_CHAT_WARNING_USER


@dp.my_chat_member_handler(old_member_status=[ChatMemberStatus.KICKED, ChatMemberStatus.LEFT], new_member_status=[ChatMemberStatus.MEMBER])
async def on_new_entered_chat(my_chat_member: types.ChatMemberUpdated):
    chat = my_chat_member.chat
    chat_id = chat.id
    db_chat = get_chat_from_group_chat_id(chat_id)
    if db_chat is None:
        await bot.send_message(chat_id,
                               UNKNOWN_CHAT_WARNING_USER.format(str(chat_id)))
        await bot.leave_chat(chat_id)
        await notify_admins(UNKNOWN_CHAT_WARNING_DEV.format(str(chat_id)))
    else:
        # add new chat admins to get them private bot access
        admins = await chat.get_administrators()
        update_res = add_admins(admins, chat_id)
        if update_res == 'added':
            admins = list(map(
                lambda admin: f'<code>{admin.user.id}</code>, @{admin.user.username}', admins))
            admins = ';\n'.join(admins)
            ans = (
                f'Добавлены новые юзеры для чата с <code>{chat_id=}</code>:\n'
                f'{admins}'
            )
            await notify_admins(ans)
