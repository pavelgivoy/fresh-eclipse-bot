from aiogram import types

from loader import dp
from database.methods.guild import set_alliance_owner
from parsers.captures import parse_set_alliance_owner_command
from utils.funcs.notify_admins import notify_admins
from utils.game_staff.answers import FORCE_UPDATE_OWNER_DONE, FORCE_UPDATE_OWNER_ERROR_DEV, FORCE_UPDATE_OWNER_ERROR_USER, FORCE_UPDATE_OWNER_WRONG_ARGS, GUILD_UNKNOWN, UNKNOWN_CAPTURE


@dp.message_handler(commands=['set_alliance_owner'], chat_groups=['super'])
async def process_set_alliance_owner(message: types.Message):
    arg_list = message.get_args().split()
    code, new_owner = parse_set_alliance_owner_command(arg_list)
    if not code or not new_owner:
        await message.answer(FORCE_UPDATE_OWNER_WRONG_ARGS)
        return

    update_res = set_alliance_owner(code, new_owner)
    if update_res == 'alliance_not_found':
        await message.answer(UNKNOWN_CAPTURE.format(code))
    elif update_res == 'guild_not_found':
        await message.answer(GUILD_UNKNOWN.format(new_owner))
    elif update_res == 'error':
        await notify_admins(FORCE_UPDATE_OWNER_ERROR_DEV)
        await message.answer(FORCE_UPDATE_OWNER_ERROR_USER)
    else:
        await message.answer(FORCE_UPDATE_OWNER_DONE)
