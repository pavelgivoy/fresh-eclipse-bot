from traceback import format_exc

from aiogram import types

from database.methods.chat import get_all
from loader import dp, bot
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import BROADCAST_DONE, BROADCAST_ERROR


@dp.message_handler(commands=['broadcast'],
                    chat_groups=['super'])
async def process_broadcast(message: types.Message):
    msg = message.get_args()
    if not msg:
        await message.answer('И что же вы хотите сказать?')
        return
    chats = get_all(groups=['war', 'admin', 'allowed'])

    chat_id = None
    try:
        for chat in chats:
            chat_id = chat.id
            await bot.send_message(chat_id, msg)
    except Exception:
        await notify_admins(BROADCAST_ERROR.format(chat_id, format_exc()))
    await message.answer(BROADCAST_DONE)
