from aiogram import types

from loader import dp
from database.methods import captures, chat, guild
from parsers.chats import parse_add_chat_command
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import CHAT_ADDED, CHAT_ADDING_ERROR_DEV, CHAT_KNOWN, GUILD_UNKNOWN, NO_CHAT_ID, UNKNOWN_CAPTURE


@dp.message_handler(commands=['add_chat'], chat_groups=['super'])
async def process_add(message: types.Message):
    chat_id, group, guild_tag, alliance_code = parse_add_chat_command(
        message)
    if not chat_id:
        await message.answer(NO_CHAT_ID)
        return

    cur_chat = chat.get_chat_from_group_chat_id(chat_id)
    if cur_chat:
        await message.answer(CHAT_KNOWN.format(str(chat_id)))
        return

    if guild_tag:
        cur_guild = guild.get(guild_tag)
        if not cur_guild:
            await message.answer(GUILD_UNKNOWN.format(guild_tag))
            return

    if not group:
        group = 'allowed'  # default group if chat is adding manually

    alliance_id = None
    if alliance_code:
        alliance = captures.get_by_code(alliance_code)
        if not alliance:
            await message.answer(UNKNOWN_CAPTURE.format(alliance_code))
            return
        alliance_id = alliance.id

    update_res = chat.add(chat_id, group, guild_tag, alliance_id)
    if update_res == 'error':
        await notify_admins(CHAT_ADDING_ERROR_DEV)
    else:
        await message.answer(CHAT_ADDED)
